"""
Utility functions for the Telegram bot
"""
import logging
import os
import tempfile
import aiohttp
from typing import Optional

logger = logging.getLogger(__name__)

async def download_file(url: str, filename: Optional[str] = None) -> str:
    """Download a file from URL to temporary location"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                
                # Create temporary file
                if filename:
                    temp_path = os.path.join(tempfile.gettempdir(), filename)
                else:
                    temp_file = tempfile.NamedTemporaryFile(delete=False)
                    temp_path = temp_file.name
                    temp_file.close()
                
                # Write content to file
                with open(temp_path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(1024):
                        f.write(chunk)
                
                logger.info(f"Downloaded file to: {temp_path}")
                return temp_path
                
    except Exception as e:
        logger.error(f"Error downloading file from {url}: {e}")
        raise Exception(f"Failed to download file: {str(e)}")

def format_error_message(service_name: str, error_message: str) -> str:
    """Format error messages for user display"""
    return (
        f"❌ **{service_name} Error**\n\n"
        f"Sorry, I encountered an issue:\n"
        f"`{error_message}`\n\n"
        f"Please try again later or contact support if the problem persists."
    )

def validate_file_size(file_size: int, max_size: int = 20 * 1024 * 1024) -> bool:
    """Validate if file size is within limits"""
    return file_size <= max_size

def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    return os.path.splitext(filename.lower())[1]

def is_supported_image_format(filename: str) -> bool:
    """Check if file is a supported image format"""
    supported_formats = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    return get_file_extension(filename) in supported_formats

def is_supported_video_format(filename: str) -> bool:
    """Check if file is a supported video format"""
    supported_formats = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
    return get_file_extension(filename) in supported_formats

def truncate_text(text: str, max_length: int = 4000) -> str:
    """Truncate text to fit Telegram message limits"""
    if len(text) <= max_length:
        return text
    
    # Try to truncate at word boundary
    truncated = text[:max_length-3]
    last_space = truncated.rfind(' ')
    
    if last_space > max_length * 0.8:  # If we can find a space in the last 20%
        truncated = truncated[:last_space]
    
    return truncated + "..."

def format_duration(seconds: int) -> str:
    """Format duration in seconds to human readable format"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}m {secs}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations"""
    # Remove or replace unsafe characters
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    
    # Limit length
    if len(filename) > 100:
        name, ext = os.path.splitext(filename)
        filename = name[:100-len(ext)] + ext
    
    return filename

def create_progress_bar(current: int, total: int, length: int = 20) -> str:
    """Create a text-based progress bar"""
    if total == 0:
        return "▓" * length
    
    progress = current / total
    filled_length = int(length * progress)
    bar = "▓" * filled_length + "░" * (length - filled_length)
    percentage = progress * 100
    
    return f"[{bar}] {percentage:.1f}%"

async def cleanup_temp_files(*file_paths: str) -> None:
    """Clean up temporary files"""
    for file_path in file_paths:
        try:
            if file_path and os.path.exists(file_path):
                os.unlink(file_path)
                logger.debug(f"Cleaned up temporary file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to clean up {file_path}: {e}")

def extract_command_args(text: str, command: str) -> str:
    """Extract arguments from a command message"""
    if text.startswith(f"/{command}"):
        return text[len(f"/{command}"):].strip()
    return text.strip()

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    size_float = float(size_bytes)
    while size_float >= 1024 and i < len(size_names) - 1:
        size_float /= 1024
        i += 1
    
    return f"{size_float:.1f} {size_names[i]}"
