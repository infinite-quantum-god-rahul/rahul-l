#!/usr/bin/env python
"""
Browser-Friendly HTTPS Server
=============================

Creates an HTTPS server with a certificate that browsers will accept more easily.
"""

import os
import sys
import django
from django.core.management import execute_from_command_line
import ssl
import subprocess

def create_browser_friendly_cert():
    """Create a certificate that browsers will accept"""
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID, ExtendedKeyUsageOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        import datetime
        
        print("🔐 Creating browser-friendly certificate...")
        
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # Create certificate with more complete information
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "SML777 Development"),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "IT Department"),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.now(datetime.timezone.utc)
        ).not_valid_after(
            datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.DNSName("127.0.0.1"),
                x509.IPAddress("127.0.0.1"),
            ]),
            critical=False,
        ).add_extension(
            x509.ExtendedKeyUsage([
                ExtendedKeyUsageOID.SERVER_AUTH,
            ]),
            critical=False,
        ).add_extension(
            x509.KeyUsage(
                key_cert_sign=False,
                crl_sign=False,
                key_encipherment=True,
                key_agreement=False,
                digital_signature=True,
                content_commitment=False,
                data_encipherment=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=False,
        ).sign(private_key, hashes.SHA256())
        
        # Save certificate and key
        with open('localhost.pem', "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        with open('localhost-key.pem', "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        print("✅ Browser-friendly certificate created!")
        return True
        
    except ImportError:
        print("❌ Cryptography library not available.")
        return False

def start_browser_friendly_https():
    """Start HTTPS server with browser-friendly certificate"""
    
    print("🚀 Starting Browser-Friendly HTTPS Server...")
    
    # Create certificate
    if not create_browser_friendly_cert():
        print("❌ Cannot create certificate. Starting HTTP server instead...")
        os.system("python manage.py runserver 127.0.0.1:8000")
        return
    
    try:
        print("🔒 Starting HTTPS server on https://localhost:8001/")
        print("🌐 Try these URLs:")
        print("   - https://localhost:8001/")
        print("   - https://127.0.0.1:8001/")
        print("⚠️  If you see a security warning:")
        print("   1. Click 'Advanced'")
        print("   2. Click 'Proceed to localhost (unsafe)'")
        print("🛑 Press Ctrl+C to stop the server")
        
        # Use django-extensions runserver_plus with SSL
        cmd = [
            'python', 'manage.py', 'runserver_plus',
            '--cert-file', 'localhost.pem',
            '--key-file', 'localhost-key.pem',
            'localhost:8001'
        ]
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped.")
    except Exception as e:
        print(f"❌ Error starting HTTPS server: {e}")
        print("🔄 Falling back to HTTP server...")
        os.system("python manage.py runserver 127.0.0.1:8000")
    finally:
        # Clean up certificate files
        try:
            if os.path.exists('localhost.pem'):
                os.remove('localhost.pem')
            if os.path.exists('localhost-key.pem'):
                os.remove('localhost-key.pem')
        except:
            pass

if __name__ == '__main__':
    start_browser_friendly_https()
