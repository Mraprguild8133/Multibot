"""
Telegram bot command and message handlers
"""
import logging
import os
import tempfile
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from bot.services.gemini_service import GeminiService
from bot.services.youtube_service import YouTubeService
from bot.services.removebg_service import RemoveBgService
from bot.services.tmdb_service import TMDBService
from bot.services.vision_service import VisionService
from bot.utils.helpers import download_file, format_error_message

logger = logging.getLogger(__name__)

# Initialize services
gemini_service = GeminiService()
youtube_service = YouTubeService()
removebg_service = RemoveBgService()
tmdb_service = TMDBService()
vision_service = VisionService()

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    welcome_message = """
🤖 **Welcome to the Comprehensive AI Bot!**

I can help you with:

🧠 **AI Assistant** - `/ai <your message>`
🎥 **YouTube Search** - `/youtube <search query>`
🎬 **Movie Search** - `/movie <movie name>`
🖼️ **Remove Background** - `/removebg` (with image)
👁️ **Image/Video Analysis** - Send me any image or video

**Other Commands:**
/help - Show this help message

Just send me a message or upload an image/video to get started!
    """
    await update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN)

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_message = """
🤖 **Bot Commands & Features:**

**🧠 AI Assistant:**
`/ai <your question>` - Chat with Gemini AI
Example: `/ai What is quantum computing?`

**🎥 YouTube Search:**
`/youtube <search query>` - Find YouTube videos
Example: `/youtube python tutorials`

**🎬 Movie Search:**
`/movie <movie name>` - Get movie details from TMDB
Example: `/movie The Matrix`

**🖼️ Background Removal:**
1. Send `/removebg` command
2. Upload an image
3. Get image with background removed

**👁️ Image/Video Analysis:**
- Send any image or video directly
- Get AI-powered analysis using Google Vision
- Works with photos, screenshots, documents, etc.

**💡 Tips:**
- You can send images/videos without any command
- All file uploads are analyzed automatically
- Use clear, specific queries for better results
    """
    await update.message.reply_text(help_message, parse_mode=ParseMode.MARKDOWN)

async def gemini_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ai command for Gemini AI assistant"""
    if not context.args:
        await update.message.reply_text("Please provide a message after /ai command.\nExample: `/ai What is artificial intelligence?`", parse_mode=ParseMode.MARKDOWN)
        return

    user_message = " ".join(context.args)
    
    try:
        # Send typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        response = await gemini_service.generate_response(user_message)
        await update.message.reply_text(f"🧠 **AI Response:**\n\n{response}", parse_mode=ParseMode.MARKDOWN)
        
    except Exception as e:
        logger.error(f"Error in Gemini handler: {e}")
        await update.message.reply_text(format_error_message("AI Assistant", str(e)))

async def youtube_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /youtube command for video search"""
    if not context.args:
        await update.message.reply_text("Please provide a search query after /youtube command.\nExample: `/youtube python programming`", parse_mode=ParseMode.MARKDOWN)
        return

    search_query = " ".join(context.args)
    
    try:
        # Send typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        videos = await youtube_service.search_videos(search_query)
        
        if not videos:
            await update.message.reply_text("No videos found for your search query.")
            return
        
        response = f"🎥 **YouTube Search Results for:** `{search_query}`\n\n"
        
        for i, video in enumerate(videos[:5], 1):
            response += f"**{i}. {video['title']}**\n"
            response += f"👤 {video['channel']}\n"
            response += f"👀 {video['views']} views\n"
            response += f"🔗 https://youtube.com/watch?v={video['video_id']}\n\n"
        
        await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
        
    except Exception as e:
        logger.error(f"Error in YouTube handler: {e}")
        await update.message.reply_text(format_error_message("YouTube Search", str(e)))

async def movie_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /movie command for movie search"""
    if not context.args:
        await update.message.reply_text("Please provide a movie name after /movie command.\nExample: `/movie The Matrix`", parse_mode=ParseMode.MARKDOWN)
        return

    movie_name = " ".join(context.args)
    
    try:
        # Send typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        movie = await tmdb_service.search_movie(movie_name)
        
        if not movie:
            await update.message.reply_text(f"No movie found for: `{movie_name}`", parse_mode=ParseMode.MARKDOWN)
            return
        
        # Format movie details
        response = f"🎬 **{movie['title']}** ({movie['year']})\n\n"
        response += f"⭐ **Rating:** {movie['rating']}/10\n"
        response += f"📅 **Release Date:** {movie['release_date']}\n"
        response += f"🎭 **Genres:** {', '.join(movie['genres'])}\n"
        response += f"⏱️ **Runtime:** {movie['runtime']} minutes\n\n"
        response += f"📝 **Overview:**\n{movie['overview']}\n\n"
        
        if movie['poster_url']:
            # Send poster image
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=movie['poster_url'],
                caption=response,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
        
    except Exception as e:
        logger.error(f"Error in movie handler: {e}")
        await update.message.reply_text(format_error_message("Movie Search", str(e)))

async def removebg_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /removebg command for background removal"""
    await update.message.reply_text(
        "🖼️ **Background Removal Service**\n\n"
        "Please upload an image and I'll remove the background for you!\n\n"
        "📝 **Supported formats:** JPG, PNG, GIF, BMP, WebP\n"
        "📏 **Max file size:** 20MB",
        parse_mode=ParseMode.MARKDOWN
    )

async def vision_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle image and video uploads for analysis"""
    try:
        # Send typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        file_obj = None
        file_type = None
        
        # Determine file type and get file object
        if update.message.photo:
            file_obj = await context.bot.get_file(update.message.photo[-1].file_id)
            file_type = "image"
        elif update.message.video:
            file_obj = await context.bot.get_file(update.message.video.file_id)
            file_type = "video"
        
        if not file_obj:
            await update.message.reply_text("Unable to process the uploaded file.")
            return
        
        # Download file to temporary location
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            await file_obj.download_to_drive(temp_file.name)
            temp_path = temp_file.name
        
        try:
            # Check if user requested background removal
            if (update.message.caption and "/removebg" in update.message.caption.lower()) or \
               (hasattr(context, 'user_data') and context.user_data and context.user_data.get('waiting_for_removebg')):
                
                if file_type == "image":
                    # Process background removal
                    result_path = await removebg_service.remove_background(temp_path)
                    
                    if result_path:
                        with open(result_path, 'rb') as result_file:
                            await context.bot.send_photo(
                                chat_id=update.effective_chat.id,
                                photo=result_file,
                                caption="🖼️ **Background removed successfully!**",
                                parse_mode=ParseMode.MARKDOWN
                            )
                        os.unlink(result_path)
                    else:
                        await update.message.reply_text("Failed to remove background. Please try with a different image.")
                else:
                    await update.message.reply_text("Background removal only works with images, not videos.")
                
                # Clear the waiting state
                if hasattr(context, 'user_data') and context.user_data:
                    context.user_data.pop('waiting_for_removebg', None)
            
            else:
                # Regular image/video analysis
                analysis = ""
                if file_type == "image":
                    analysis = await vision_service.analyze_image(temp_path)
                elif file_type == "video":
                    analysis = await vision_service.analyze_video(temp_path)
                
                if analysis:
                    # Truncate analysis if too long and escape markdown
                    if len(analysis) > 3800:
                        analysis = analysis[:3800] + "..."
                    
                    # Remove problematic markdown characters
                    analysis = analysis.replace('*', '').replace('_', '').replace('[', '').replace(']', '')
                    
                    response = f"👁️ {file_type.title()} Analysis:\n\n{analysis}"
                    await update.message.reply_text(response)
                else:
                    await update.message.reply_text(f"Unable to analyze the {file_type}. Please try again.")
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    except Exception as e:
        logger.error(f"Error in vision handler: {e}")
        await update.message.reply_text(format_error_message("File Analysis", str(e)))

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages (fallback to Gemini AI)"""
    user_message = update.message.text
    
    try:
        # Send typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        response = await gemini_service.generate_response(user_message)
        await update.message.reply_text(f"🧠 {response}")
        
    except Exception as e:
        logger.error(f"Error in text handler: {e}")
        await update.message.reply_text(
            "I'm having trouble processing your message right now. "
            "You can try using specific commands like /ai, /youtube, or /movie."
        )
