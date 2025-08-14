"""
YouTube Data API service for video search
"""
import logging
import os
import requests
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class YouTubeService:
    """Service for YouTube video search using YouTube Data API"""
    
    def __init__(self):
        """Initialize YouTube service"""
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            logger.error("YOUTUBE_API_KEY environment variable not set")
            raise ValueError("YouTube API key is required")
        
        self.base_url = "https://www.googleapis.com/youtube/v3"
    
    async def search_videos(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search for YouTube videos"""
        try:
            # Search for videos
            search_url = f"{self.base_url}/search"
            search_params = {
                'part': 'snippet',
                'q': query,
                'type': 'video',
                'maxResults': max_results,
                'key': self.api_key,
                'order': 'relevance'
            }
            
            response = requests.get(search_url, params=search_params)
            response.raise_for_status()
            
            search_data = response.json()
            
            if 'items' not in search_data:
                return []
            
            # Get video statistics
            video_ids = [item['id']['videoId'] for item in search_data['items']]
            videos_url = f"{self.base_url}/videos"
            videos_params = {
                'part': 'statistics,contentDetails',
                'id': ','.join(video_ids),
                'key': self.api_key
            }
            
            stats_response = requests.get(videos_url, params=videos_params)
            stats_response.raise_for_status()
            
            stats_data = stats_response.json()
            
            # Combine search results with statistics
            videos = []
            for i, item in enumerate(search_data['items']):
                video_id = item['id']['videoId']
                snippet = item['snippet']
                
                # Find corresponding statistics
                stats = {}
                for stats_item in stats_data.get('items', []):
                    if stats_item['id'] == video_id:
                        stats = stats_item['statistics']
                        break
                
                video_info = {
                    'video_id': video_id,
                    'title': snippet['title'],
                    'channel': snippet['channelTitle'],
                    'description': snippet['description'][:200] + '...' if len(snippet['description']) > 200 else snippet['description'],
                    'published_at': snippet['publishedAt'],
                    'thumbnail': snippet['thumbnails']['medium']['url'],
                    'views': self._format_number(stats.get('viewCount', '0')),
                    'likes': self._format_number(stats.get('likeCount', '0')),
                    'comments': self._format_number(stats.get('commentCount', '0'))
                }
                
                videos.append(video_info)
            
            return videos
            
        except requests.RequestException as e:
            logger.error(f"Error searching YouTube videos: {e}")
            raise Exception(f"Failed to search YouTube: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in YouTube search: {e}")
            raise Exception(f"YouTube search failed: {str(e)}")
    
    def _format_number(self, num_str: str) -> str:
        """Format large numbers with K, M, B suffixes"""
        try:
            num = int(num_str)
            if num >= 1_000_000_000:
                return f"{num / 1_000_000_000:.1f}B"
            elif num >= 1_000_000:
                return f"{num / 1_000_000:.1f}M"
            elif num >= 1_000:
                return f"{num / 1_000:.1f}K"
            else:
                return str(num)
        except (ValueError, TypeError):
            return "0"
