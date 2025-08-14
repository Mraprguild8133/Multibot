# Comprehensive Telegram Bot

A powerful multi-feature Telegram bot with AI assistance, YouTube search, movie information, background removal, and image/video analysis capabilities.

## Features

### 🤖 AI Assistant (Gemini)
- **Command**: `/ai <your question>`
- **Example**: `/ai What is quantum computing?`
- Chat with Google's Gemini AI for any questions or conversations

### 🎥 YouTube Video Search
- **Command**: `/youtube <search query>`
- **Example**: `/youtube python tutorials`
- Find and get detailed information about YouTube videos including:
  - Video title and channel
  - View count and statistics
  - Direct links to videos

### 🎬 Movie Search & Information
- **Command**: `/movie <movie name>`
- **Example**: `/movie The Matrix`
- Get comprehensive movie details including:
  - Movie poster images
  - Rating, release date, runtime
  - Cast, director, genres
  - Plot overview and production info

### 🖼️ Background Removal
- **Command**: `/removebg` then upload an image
- Automatically removes backgrounds from uploaded images
- Supports JPG, PNG, GIF, BMP, WebP formats
- Returns processed image with transparent background

### 👁️ Enhanced Image & Video Analysis
- **Usage**: Send any image or video directly to the bot
- **Dual AI Analysis**: Combines Google Vision API + Gemini AI for comprehensive results
- **Google Vision Features**:
  - Object and landmark detection
  - Text extraction (OCR) from images
  - Face detection and counting
  - Logo and brand recognition
- **Gemini AI Analysis**:
  - Detailed scene descriptions
  - Context and mood analysis
  - Color and composition insights
  - Creative interpretation

### 💬 Natural Conversation
- Send any text message for AI-powered responses
- Bot automatically responds to regular messages using Gemini AI
- No commands needed for basic conversation

## Getting Started

1. **Find Your Bot**: Search for your bot's username on Telegram
2. **Start the Bot**: Send `/start` to see the welcome message
3. **Get Help**: Send `/help` for detailed command information
4. **Start Using**: Try any of the commands or just send a message!

## Example Usage

```
/start                           # Welcome message
/help                           # Detailed help
/ai How does machine learning work?
/youtube best cooking recipes
/movie Inception
/removebg                       # Then upload an image
Send any image or video         # Automatic analysis
Hello, how are you?            # Natural conversation
```

## Supported File Formats

**Images**: JPG, JPEG, PNG, GIF, BMP, WebP (max 20MB)
**Videos**: MP4, AVI, MOV, MKV, WMV (max 20MB)

## Features Status

✅ **Gemini AI Assistant** - Fully functional
✅ **YouTube Search** - Fully functional  
✅ **Movie Search (TMDB)** - Fully functional with updated API key
✅ **Background Removal** - Fully functional
✅ **Enhanced Image Analysis** - Google Vision API + Gemini AI working together
✅ **Video Analysis** - Fully functional using Gemini AI
✅ **Natural Conversations** - Fully functional

## Technical Details

- **Framework**: python-telegram-bot 21.7
- **AI Engine**: Google Gemini 2.5 Flash/Pro
- **APIs**: YouTube Data API v3, TMDB API, Remove.bg API
- **Language**: Python 3.11
- **Hosting**: Replit with continuous deployment

Your bot is now live and ready to use!