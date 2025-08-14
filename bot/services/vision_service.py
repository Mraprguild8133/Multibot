"""
Enhanced image and video analysis service using Google Vision API and Gemini AI
"""
import logging
import os
import json
import tempfile
from bot.services.gemini_service import GeminiService

logger = logging.getLogger(__name__)

class VisionService:
    """Service for image and video analysis using Google Vision API and Gemini AI"""
    
    def __init__(self):
        """Initialize Vision service"""
        # Check for Google Vision API credentials
        credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if credentials_json:
            try:
                # Parse JSON credentials and save to temporary file
                credentials_data = json.loads(credentials_json)
                
                # Create temporary credentials file
                with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                    json.dump(credentials_data, f)
                    credentials_path = f.name
                
                # Set environment variable for Google Cloud client
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
                
                # Import and initialize Vision client
                from google.cloud import vision
                self.vision_client = vision.ImageAnnotatorClient()
                self.vision_available = True
                logger.info("Google Vision API initialized successfully")
                
            except Exception as e:
                logger.warning(f"Failed to initialize Google Vision API: {e}")
                self.vision_client = None
                self.vision_available = False
        else:
            logger.info("Google Vision API credentials not provided")
            self.vision_client = None
            self.vision_available = False
        
        # Initialize Gemini as primary/fallback AI
        self.gemini_service = GeminiService()
        logger.info("Vision service initialized")
    
    async def analyze_image(self, image_path: str) -> str:
        """Analyze an image using Google Vision API and Gemini AI"""
        try:
            if self.vision_available:
                # Use combined Google Vision + Gemini analysis
                return await self._analyze_with_combined_vision(image_path)
            else:
                # Fallback to Gemini only
                return await self._analyze_with_gemini_image(image_path)
        except Exception as e:
            logger.error(f"Error in image analysis: {e}")
            # Try Gemini fallback if Vision fails
            try:
                return await self._analyze_with_gemini_image(image_path)
            except Exception as fallback_error:
                logger.error(f"Fallback analysis also failed: {fallback_error}")
                return "Unable to analyze the image. Please try again later."
    
    async def analyze_video(self, video_path: str) -> str:
        """Analyze a video using Gemini (Vision API doesn't support video directly)"""
        try:
            return await self.gemini_service.analyze_video_with_gemini(video_path)
        except Exception as e:
            logger.error(f"Error in video analysis: {e}")
            return "Unable to analyze the video. Please try again later."
    

    async def _analyze_with_combined_vision(self, image_path: str) -> str:
        """Analyze image using both Google Vision API and Gemini AI"""
        try:
            # Get Google Vision analysis
            vision_results = await self._analyze_with_google_vision(image_path)
            
            # Get Gemini analysis
            gemini_analysis = await self._analyze_with_gemini_image(image_path)
            
            # Combine results
            if vision_results and gemini_analysis:
                combined = f"{vision_results}\n\n**AI Analysis:**\n{gemini_analysis}"
                return combined
            elif vision_results:
                return vision_results
            else:
                return gemini_analysis
                
        except Exception as e:
            logger.error(f"Combined vision analysis failed: {e}")
            # Fallback to Gemini only
            return await self._analyze_with_gemini_image(image_path)
    
    async def _analyze_with_google_vision(self, image_path: str) -> str:
        """Analyze image using Google Vision API"""
        try:
            from google.cloud import vision
            
            # Read image file
            with open(image_path, 'rb') as image_file:
                content = image_file.read()
            
            image = vision.Image(content=content)
            analysis_results = []
            
            # Label detection (objects)
            try:
                response = self.vision_client.label_detection(image=image)
                if response.label_annotations:
                    labels = [label.description for label in response.label_annotations[:5]]
                    analysis_results.append(f"**Objects Detected:** {', '.join(labels)}")
            except Exception as e:
                logger.warning(f"Label detection failed: {e}")
            
            # Text detection (OCR)
            try:
                response = self.vision_client.text_detection(image=image)
                if response.text_annotations:
                    detected_text = response.text_annotations[0].description.strip()
                    if detected_text and len(detected_text) > 3:
                        # Limit text length
                        if len(detected_text) > 200:
                            detected_text = detected_text[:200] + "..."
                        analysis_results.append(f"**Text Found:** {detected_text}")
            except Exception as e:
                logger.warning(f"Text detection failed: {e}")
            
            # Face detection
            try:
                response = self.vision_client.face_detection(image=image)
                if response.face_annotations:
                    face_count = len(response.face_annotations)
                    analysis_results.append(f"**Faces Detected:** {face_count}")
            except Exception as e:
                logger.warning(f"Face detection failed: {e}")
            
            # Landmark detection
            try:
                response = self.vision_client.landmark_detection(image=image)
                if response.landmark_annotations:
                    landmarks = [landmark.description for landmark in response.landmark_annotations[:3]]
                    analysis_results.append(f"**Landmarks:** {', '.join(landmarks)}")
            except Exception as e:
                logger.warning(f"Landmark detection failed: {e}")
            
            # Logo detection
            try:
                response = self.vision_client.logo_detection(image=image)
                if response.logo_annotations:
                    logos = [logo.description for logo in response.logo_annotations[:3]]
                    analysis_results.append(f"**Logos:** {', '.join(logos)}")
            except Exception as e:
                logger.warning(f"Logo detection failed: {e}")
            
            if analysis_results:
                return "\n".join(analysis_results)
            else:
                return ""
                
        except Exception as e:
            logger.error(f"Google Vision analysis failed: {e}")
            return ""
    
    async def _analyze_with_gemini_image(self, image_path: str) -> str:
        """Analyze image using Gemini AI"""
        try:
            prompt = (
                "Analyze this image thoroughly and provide detailed information about:\n"
                "- What objects, people, or scenes you can see\n"
                "- Any text that might be visible\n"
                "- The setting, mood, or context\n"
                "- Any notable features, colors, or composition elements\n"
                "- If applicable, identify any landmarks, brands, or recognizable elements"
            )
            return await self.gemini_service.analyze_image_with_gemini(image_path, prompt)
        except Exception as e:
            logger.error(f"Gemini image analysis failed: {e}")
            raise
