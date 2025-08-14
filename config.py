"""
Configuration settings for the Telegram Bot
"""
import os

class Config:
    """Configuration class for API keys and settings"""
    
    # Telegram Bot
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    
    # Gemini AI
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # YouTube Data API
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    
    # Remove.bg API
    REMOVEBG_API_KEY = os.getenv("REMOVEBG_API_KEY")
    
    # TMDB API
    TMDB_API_KEY = os.getenv("TMDB_API_KEY")
    
    # Google Vision API
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    # Default settings
    MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB
    SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    SUPPORTED_VIDEO_FORMATS = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
