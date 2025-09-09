#!/usr/bin/env python
"""
Simple HTTPS Server for Django
==============================

This script creates a simple HTTPS server that can serve Django.
"""

import os
import sys
import django
from django.core.wsgi import get_wsgi_application
import ssl
import tempfile
import subprocess

def create_self_signed_cert():
    """Create a self-signed certificate"""
    try:
        # Try to use OpenSSL if available
        result = subprocess.run(['openssl', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("OpenSSL found, generating certificate...")
            
            # Create certificate
            subprocess.run([
                'openssl', 'req', '-x509', '-newkey', 'rsa:2048', 
                '-keyout', 'key.pem', '-out', 'cert.pem', 
                '-days', '365', '-nodes', '-subj',
                '/C=US/ST=State/L=City/O=Organization/CN=127.0.0.1'
            ], check=True)
            
            return True
    except:
        pass
    
    # If OpenSSL not available, create a simple certificate
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        import datetime
        
        print("Using cryptography library to generate certificate...")
        
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
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Organization"),
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
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
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
        
        return True
        
    except ImportError:
        print("Neither OpenSSL nor cryptography library available.")
        return False

def run_https_server():
    """Run Django with HTTPS"""
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
    django.setup()
    
    # Get WSGI application
    application = get_wsgi_application()
    
    # Create self-signed certificate
    if not create_self_signed_cert():
        print("Cannot create certificate. Falling back to HTTP on port 8002...")
        os.system("python manage.py runserver 127.0.0.1:8002")
        return
    
    # Create HTTPS server
    from http.server import HTTPServer
    from django.core.handlers.wsgi import WSGIHandler
    
    class WSGIHTTPServer(HTTPServer):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.wsgi_app = WSGIHandler()
    
    # Create server
    server_address = ('127.0.0.1', 8001)
    httpd = WSGIHTTPServer(server_address, lambda *args, **kwargs: None)
    
    # Create SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')
    
    # Wrap socket with SSL
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    
    print("🔒 HTTPS Django server running at https://127.0.0.1:8001/")
    print("⚠️  You may see a security warning - click 'Advanced' and 'Proceed to 127.0.0.1'")
    print("🛑 Press Ctrl+C to stop the server")
    
    try:
        # Start server
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped.")
    finally:
        # Clean up certificate files
        try:
            os.remove('cert.pem')
            os.remove('key.pem')
        except:
            pass

if __name__ == '__main__':
    run_https_server()

