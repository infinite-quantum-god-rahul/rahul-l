#!/usr/bin/env python
"""
Simple HTTPS Server using Django's runserver with SSL
=====================================================

This uses Django's built-in development server with SSL support.
"""

import os
import sys
import django
from django.core.management import execute_from_command_line
import ssl
import socket

def create_self_signed_cert():
    """Create a self-signed certificate"""
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        import datetime
        
        print("🔐 Creating self-signed certificate...")
        
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # Create certificate
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "State"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "City"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "SML777"),
            x509.NameAttribute(NameOID.COMMON_NAME, "127.0.0.1"),
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
                x509.DNSName("127.0.0.1"),
                x509.DNSName("localhost"),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256())
        
        # Save certificate and key
        with open('cert.pem', "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        with open('key.pem', "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        print("✅ Certificate created: cert.pem and key.pem")
        return True
        
    except ImportError:
        print("❌ Cryptography library not available.")
        return False

def run_https_server():
    """Run Django with HTTPS using runserver"""
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
    django.setup()
    
    # Create self-signed certificate
    if not create_self_signed_cert():
        print("❌ Cannot create certificate. Using HTTP instead...")
        os.system("python manage.py runserver 127.0.0.1:8000")
        return
    
    print("🚀 Starting Django HTTPS server...")
    print("🔒 Server will be available at: https://127.0.0.1:8001/")
    print("⚠️  You may see a security warning - click 'Advanced' and 'Proceed to 127.0.0.1'")
    print("🛑 Press Ctrl+C to stop the server")
    
    # Use Django's runserver with custom SSL
    try:
        # Monkey patch Django's runserver to use SSL
        from django.core.servers.basehttp import WSGIServer
        from django.core.management.commands.runserver import Command as RunserverCommand
        
        # Create SSL context
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain('cert.pem', 'key.pem')
        
        # Override the server creation
        original_server_class = WSGIServer
        
        class SSLWSGIServer(WSGIServer):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.socket = context.wrap_socket(self.socket, server_side=True)
        
        # Replace the server class
        WSGIServer = SSLWSGIServer
        
        # Run the server
        execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8001'])
        
    except Exception as e:
        print(f"❌ Error with SSL server: {e}")
        print("🔄 Falling back to HTTP server...")
        os.system("python manage.py runserver 127.0.0.1:8000")
    finally:
        # Clean up certificate files
        try:
            if os.path.exists('cert.pem'):
                os.remove('cert.pem')
            if os.path.exists('key.pem'):
                os.remove('key.pem')
        except:
            pass

if __name__ == '__main__':
    run_https_server()
