"""
Gemini AI service for text generation and analysis
"""
import logging
import os
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

class GeminiService:
    """Service for interacting with Gemini AI"""
    
    def __init__(self):
        """Initialize Gemini client"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("GEMINI_API_KEY environment variable not set")
            raise ValueError("Gemini API key is required")
        
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"
    
    async def generate_response(self, prompt: str) -> str:
        """Generate a response using Gemini AI"""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            return response.text or "I'm sorry, I couldn't generate a response for that."
            
        except Exception as e:
            logger.error(f"Error generating Gemini response: {e}")
            raise Exception(f"Failed to get AI response: {str(e)}")
    
    async def analyze_image_with_gemini(self, image_path: str, prompt: str | None = None) -> str:
        """Analyze an image using Gemini AI"""
        try:
            if not prompt:
                prompt = "Analyze this image in detail and describe its key elements, context, and any notable aspects."
            
            with open(image_path, "rb") as f:
                image_bytes = f.read()
                
                response = self.client.models.generate_content(
                    model="gemini-2.5-pro",
                    contents=[
                        types.Part.from_bytes(
                            data=image_bytes,
                            mime_type="image/jpeg",
                        ),
                        prompt,
                    ],
                )
            
            return response.text if response.text else "Unable to analyze the image."
            
        except Exception as e:
            logger.error(f"Error analyzing image with Gemini: {e}")
            raise Exception(f"Failed to analyze image: {str(e)}")
    
    async def analyze_video_with_gemini(self, video_path: str, prompt: str | None = None) -> str:
        """Analyze a video using Gemini AI"""
        try:
            if not prompt:
                prompt = "Analyze this video in detail and describe its key elements, context, and any notable aspects."
            
            with open(video_path, "rb") as f:
                video_bytes = f.read()
                
                response = self.client.models.generate_content(
                    model="gemini-2.5-pro",
                    contents=[
                        types.Part.from_bytes(
                            data=video_bytes,
                            mime_type="video/mp4",
                        ),
                        prompt,
                    ],
                )
            
            return response.text if response.text else "Unable to analyze the video."
            
        except Exception as e:
            logger.error(f"Error analyzing video with Gemini: {e}")
            raise Exception(f"Failed to analyze video: {str(e)}")
