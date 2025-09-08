#!/usr/bin/env python
"""
Simple HTTPS Server for Django Development
Uses Python's built-in HTTPS server with a self-signed certificate.
"""

import os
import sys
import ssl
import subprocess
import threading
import time
import webbrowser

def create_self_signed_cert():
    """Create a self-signed certificate using OpenSSL."""
    try:
        # Check if OpenSSL is available
        result = subprocess.run(['openssl', 'version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("⚠️  OpenSSL not found. Using HTTP instead.")
            return False
        
        print("🔧 Creating self-signed certificate...")
        
        # Create private key
        subprocess.run([
            'openssl', 'genrsa', '-out', 'dev_key.pem', '2048'
        ], check=True, capture_output=True)
        
        # Create certificate
        subprocess.run([
            'openssl', 'req', '-new', '-x509', '-key', 'dev_key.pem', 
            '-out', 'dev_cert.pem', '-days', '365', '-subj',
            '/C=US/ST=Development/L=Local/O=Django Development/CN=127.0.0.1'
        ], check=True, capture_output=True)
        
        print("✅ Self-signed certificate created")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Error creating certificate: {e}. Using HTTP instead.")
        return False
    except FileNotFoundError:
        print("⚠️  OpenSSL not found. Using HTTP instead.")
        return False

def run_django_server():
    """Run Django development server."""
    try:
        subprocess.run([
            sys.executable, 'manage.py', 'runserver', '127.0.0.1:8001'
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Django server: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Django server stopped")

def run_https_proxy():
    """Run HTTPS proxy server."""
    try:
        import http.server
        import socketserver
        import urllib.request
        import urllib.parse
        
        class HTTPSProxyHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                self.proxy_request()
            
            def do_POST(self):
                self.proxy_request()
            
            def do_PUT(self):
                self.proxy_request()
            
            def do_DELETE(self):
                self.proxy_request()
            
            def proxy_request(self):
                # Forward request to Django server
                django_url = f"http://127.0.0.1:8001{self.path}"
                
                try:
                    # Create request
                    req = urllib.request.Request(django_url)
                    req.method = self.command
                    
                    # Copy headers
                    for header, value in self.headers.items():
                        req.add_header(header, value)
                    
                    # Handle POST data
                    if self.command in ['POST', 'PUT']:
                        content_length = int(self.headers.get('Content-Length', 0))
                        if content_length > 0:
                            post_data = self.rfile.read(content_length)
                            req.data = post_data
                    
                    # Make request to Django
                    with urllib.request.urlopen(req) as response:
                        # Send response
                        self.send_response(response.status)
                        
                        # Copy response headers
                        for header, value in response.headers.items():
                            if header.lower() not in ['connection', 'transfer-encoding']:
                                self.send_header(header, value)
                        self.end_headers()
                        
                        # Copy response body
                        self.wfile.write(response.read())
                        
                except Exception as e:
                    self.send_error(500, f"Proxy error: {e}")
            
            def log_message(self, format, *args):
                # Suppress proxy logs
                pass
        
        # Create HTTPS server
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain('dev_cert.pem', 'dev_key.pem')
        
        with socketserver.TCPServer(('127.0.0.1', 8000), HTTPSProxyHandler) as httpd:
            httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
            print("🚀 HTTPS Proxy running at https://127.0.0.1:8000/")
            print("🛑 Press Ctrl+C to stop")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 HTTPS proxy stopped")
    except Exception as e:
        print(f"❌ Error running HTTPS proxy: {e}")

def main():
    """Main function to start HTTPS server."""
    print("🔒 Starting Django HTTPS Server")
    print("=" * 50)
    
    # Create self-signed certificate
    if not create_self_signed_cert():
        print("🔄 Starting HTTP server instead...")
        try:
            subprocess.run([
                sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000'
            ], check=True)
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
        return
    
    # Start Django server in background
    django_thread = threading.Thread(target=run_django_server, daemon=True)
    django_thread.start()
    
    # Wait for Django server to start
    print("⏳ Waiting for Django server to start...")
    time.sleep(3)
    
    # Start HTTPS proxy
    try:
        run_https_proxy()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    finally:
        # Clean up certificate files
        try:
            os.remove('dev_cert.pem')
            os.remove('dev_key.pem')
            print("🧹 Cleaned up certificate files")
        except:
            pass

if __name__ == "__main__":
    main()
