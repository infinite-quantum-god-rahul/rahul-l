#!/usr/bin/env python
"""
Run Django Server with HTTPS using werkzeug
This provides proper HTTPS support for development.
"""

import os
import sys
import ssl
import django
from django.core.management import execute_from_command_line
from django.core.wsgi import get_wsgi_application
from werkzeug.serving import make_server

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

def create_self_signed_cert():
    """Create a self-signed certificate for HTTPS development."""
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        import datetime
        
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # Create certificate
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Development"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Local"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Django Development"),
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
        
        # Write certificate and key to files
        with open("dev_cert.pem", "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        with open("dev_key.pem", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        return True
    except ImportError:
        print("⚠️  cryptography library not available. Using HTTP instead.")
        return False
    except Exception as e:
        print(f"⚠️  Error creating certificate: {e}. Using HTTP instead.")
        return False

def run_https_server():
    """Run Django server with HTTPS support."""
    
    print("🔒 Setting up HTTPS server...")
    print("=" * 50)
    
    # Try to create self-signed certificate
    if create_self_signed_cert():
        print("✅ Self-signed certificate created")
        
        # Create SSL context
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain('dev_cert.pem', 'dev_key.pem')
        
        print("🌐 Starting HTTPS server at https://127.0.0.1:8000/")
        print("⚠️  Browser will show security warning - click 'Advanced' and 'Proceed'")
        print("=" * 50)
        
        try:
            # Use werkzeug to serve with HTTPS
            from werkzeug.serving import make_server
            from django.core.wsgi import get_wsgi_application
            
            application = get_wsgi_application()
            
            with make_server('127.0.0.1', 8000, application, ssl_context=context) as httpd:
                print("🚀 HTTPS Server running at https://127.0.0.1:8000/")
                print("🛑 Press Ctrl+C to stop")
                httpd.serve_forever()
                
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
        except Exception as e:
            print(f"\n❌ Error starting HTTPS server: {e}")
            print("🔄 Falling back to HTTP server...")
            run_http_server()
    else:
        print("🔄 Using HTTP server instead...")
        run_http_server()

def run_http_server():
    """Run Django server with HTTP (fallback)."""
    print("🌐 Starting HTTP server at http://127.0.0.1:8000/")
    print("=" * 50)
    
    try:
        execute_from_command_line([
            'manage.py', 
            'runserver', 
            '127.0.0.1:8000'
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")

if __name__ == "__main__":
    run_https_server()
