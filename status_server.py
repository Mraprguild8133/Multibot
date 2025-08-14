#!/usr/bin/env python3
"""
Simple status server for webhook monitoring
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
            
            status = {
                "status": "online",
                "bot": "Telegram AI Bot",
                "webhook": f"https://{os.getenv('REPLIT_DEV_DOMAIN', 'localhost')}/webhook",
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
    server = HTTPServer(('0.0.0.0', 3000), StatusHandler)
    print(f"Status server running on port 3000")
    server.serve_forever()