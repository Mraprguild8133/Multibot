#!/usr/bin/env python3
"""
Enhanced webhook server with status endpoint and Telegram bot integration
Modified to use port 5000 as default
"""

import logging
import os
import asyncio
from tornado.web import Application as TornadoApp, RequestHandler
from tornado.platform.asyncio import AsyncIOMainLoop
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bot.handlers import (
    start_handler, help_handler, gemini_handler, youtube_handler,
    movie_handler, removebg_handler, vision_handler, text_handler
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class StatusHandler(RequestHandler):
    """Status endpoint for bot health check"""
    def get(self):
        self.set_header("Content-Type", "application/json")
        self.write({
            "status": "online",
            "bot": "Telegram AI Bot",
            "webhook": f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME', 'localhost')}:5000/webhook",
            "features": [
                "AI Assistant (Gemini)",
                "YouTube Search", 
                "Movie Search (TMDB)",
                "Background Removal",
                "Enhanced Image Analysis (Vision API + Gemini)"
            ],
            "version": "2.0.0"
        })

class HealthHandler(RequestHandler):
    """Simple health check endpoint"""
    def get(self):
        self.write("OK")

async def main():
    """Start the enhanced webhook server"""
    # Get bot token from environment
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set")
        return

    # Create Telegram application
    application = Application.builder().token(bot_token).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(CommandHandler("ai", gemini_handler))
    application.add_handler(CommandHandler("youtube", youtube_handler))
    application.add_handler(CommandHandler("movie", movie_handler))
    application.add_handler(CommandHandler("removebg", removebg_handler))
    
    # Add message handlers
    application.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, vision_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    logger.info("Bot started successfully!")
    
    # Get Render URL (default: *.onrender.com)
    render_url = os.getenv("RENDER_EXTERNAL_HOSTNAME")
    if not render_url:
        logger.error("RENDER_EXTERNAL_HOSTNAME not available. Using localhost.")
        render_url = "localhost"
        
    webhook_url = f"https://{render_url}:5000/webhook"  # Using port 5000
    logger.info(f"Starting enhanced webhook server with URL: {webhook_url}")
    
    # Create web application with status endpoints
    webapp = TornadoApp([
        (r"/", StatusHandler),
        (r"/status", StatusHandler),
        (r"/health", HealthHandler),
    ])
    
    try:
        # Start the webhook
        await application.initialize()
        await application.start()
        
        # Set up webhook (now listening on port 5000)
        await application.updater.start_webhook(
            listen="0.0.0.0",
            port=5000,  # Changed to port 5000
            webhook_url=webhook_url,
            url_path="/webhook",
            app=webapp
        )
        
        logger.info("Webhook server started successfully on port 5000")
        
        # Keep running
        await application.updater.idle()
        
    except Exception as e:
        logger.error(f"Webhook server failed: {e}")
        # Fallback to polling
        logger.info("Falling back to polling mode")
        await application.run_polling(allowed_updates=["message"])

if __name__ == '__main__':
    AsyncIOMainLoop().install()
    asyncio.run(main())
