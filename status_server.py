#!/usr/bin/env python3
"""
Simple status server for webhook monitoring (Render.com compatible)
"""

import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

class StatusHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ['/', '/status', '/health']:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Use RENDER_EXTERNAL_URL if running on Render, otherwise fallback to localhost
            render_url = os.getenv('RENDER_EXTERNAL_URL', 'http://localhost')
            
            status = {
                "status": "online",
                "bot": "Telegram AI Bot",
                "webhook": f"{render_url}/webhook",  # Updated for Render
                "features": [
                    "AI Assistant (Gemini)",
                    "YouTube Search", 
                    "Movie Search (TMDB)",
                    "Background Removal",
                    "Enhanced Image Analysis"
                ],
                "version": "2.0.0"
            }
            self.wfile.write(json.dumps(status, indent=2).encode())
        else:
            self.send_error(404)

if __name__ == '__main__':
    port = int(os.getenv('PORT', '5000'))  # Render uses $PORT, default to 5000
    server = HTTPServer(('0.0.0.0', port), StatusHandler)
    print(f"Status server running on port {port}")
    server.serve_forever()
