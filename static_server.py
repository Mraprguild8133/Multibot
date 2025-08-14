#!/usr/bin/env python3
"""
Simple static file server for serving index.html and status API
"""

import os
import json
import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

class StaticHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        
        # Route handling
        if path == '/' or path == '/index.html':
            self.serve_file('index.html', 'text/html')
        elif path == '/status':
            self.serve_status()
        elif path == '/health':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_error(404)
    
    def serve_file(self, filename, content_type):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404)
    
    def serve_status(self):
        status = {
            "status": "online",
            "bot": "Telegram AI Bot",
            "webhook": f"https://{os.getenv('REPLIT_DEV_DOMAIN', 'localhost')}/webhook",
            "features": [
                "AI Assistant (Gemini)",
                "YouTube Search", 
                "Movie Search (TMDB)",
                "Background Removal",
                "Enhanced Image Analysis (Vision API + Gemini)"
            ],
            "version": "2.0.0",
            "endpoints": {
                "webhook": "/webhook",
                "status": "/status",
                "health": "/health"
            }
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(status, indent=2).encode())

if __name__ == '__main__':
    port = int(os.getenv('STATIC_PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), StaticHandler)
    print(f"Static server running on port {port}")
    print(f"Access at: http://localhost:{port}")
    server.serve_forever()