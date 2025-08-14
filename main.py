#!/usr/bin/env python3
"""
Comprehensive Telegram Bot with AI Assistant and Multiple Services
"""

import logging
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bot.handlers import (
    start_handler, help_handler, gemini_handler, youtube_handler,
    movie_handler, removebg_handler, vision_handler, text_handler
)
from config import Config

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Start the bot"""
    # Get bot token from environment
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set")
        return

    # Create application
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
    
    # Check if running on Replit with webhook support
    replit_url = os.getenv("REPLIT_DEV_DOMAIN")
    webhook_mode = os.getenv("USE_WEBHOOK", "false").lower() == "true"
    
    if replit_url:
        # Always try webhook mode on Replit
        webhook_url = f"https://{replit_url}/webhook"
        logger.info(f"Starting webhook mode with URL: {webhook_url}")
        try:
            application.run_webhook(
                listen="0.0.0.0",
                port=5000,
                webhook_url=webhook_url,
                url_path="/webhook",
                allowed_updates=["message"]
            )
        except Exception as e:
            logger.error(f"Webhook failed: {e}. Falling back to polling mode.")
            application.run_polling(allowed_updates=["message"])
    else:
        # Use polling mode for local development
        logger.info("Starting polling mode")
        application.run_polling(allowed_updates=["message"])

if __name__ == '__main__':
    main()
