"""
Remove.bg API service for background removal
"""
import logging
import os
import requests
import tempfile
from typing import Optional

logger = logging.getLogger(__name__)

class RemoveBgService:
    """Service for removing backgrounds from images using Remove.bg API"""
    
    def __init__(self):
        """Initialize Remove.bg service"""
        self.api_key = os.getenv("REMOVEBG_API_KEY")
        if not self.api_key:
            logger.error("REMOVEBG_API_KEY environment variable not set")
            raise ValueError("Remove.bg API key is required")
        
        self.api_url = "https://api.remove.bg/v1.0/removebg"
    
    async def remove_background(self, image_path: str) -> Optional[str]:
        """Remove background from an image"""
        try:
            # Read the image file
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
            
            # Prepare the request
            headers = {
                'X-Api-Key': self.api_key,
            }
            
            files = {
                'image_file': image_data,
            }
            
            data = {
                'size': 'auto',  # Options: auto, preview, full
                'format': 'png',  # Output format
                'type': 'auto',   # Type detection: auto, person, product, car
            }
            
            # Make the API request
            response = requests.post(
                self.api_url,
                headers=headers,
                files=files,
                data=data,
                timeout=30
            )
            
            response.raise_for_status()
            
            # Save the result to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
                temp_file.write(response.content)
                result_path = temp_file.name
            
            logger.info(f"Background removed successfully, saved to: {result_path}")
            return result_path
            
        except requests.RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                if e.response.status_code == 402:
                    logger.error("Remove.bg API quota exceeded")
                    raise Exception("Background removal quota exceeded. Please try again later.")
                elif e.response.status_code == 400:
                    logger.error("Invalid image format for Remove.bg")
                    raise Exception("Invalid image format. Please use JPG, PNG, or GIF.")
                else:
                    logger.error(f"Remove.bg API error: {e.response.status_code} - {e.response.text}")
                    raise Exception(f"Background removal failed: {e.response.status_code}")
            else:
                logger.error(f"Network error with Remove.bg API: {e}")
                raise Exception("Network error during background removal")
        
        except Exception as e:
            logger.error(f"Unexpected error in background removal: {e}")
            raise Exception(f"Background removal failed: {str(e)}")
    
    def get_account_info(self) -> dict:
        """Get Remove.bg account information and usage"""
        try:
            headers = {
                'X-Api-Key': self.api_key,
            }
            
            response = requests.get(
                'https://api.remove.bg/v1.0/account',
                headers=headers,
                timeout=10
            )
            
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Error getting Remove.bg account info: {e}")
            return {}
