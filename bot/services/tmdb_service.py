"""
TMDB (The Movie Database) API service for movie search
"""
import logging
import os
import requests
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)

class TMDBService:
    """Service for movie search using TMDB API"""
    
    def __init__(self):
        """Initialize TMDB service"""
        self.api_key = os.getenv("TMDB_API_KEY")
        if not self.api_key:
            logger.error("TMDB_API_KEY environment variable not set")
            raise ValueError("TMDB API key is required")
        
        self.base_url = "https://api.themoviedb.org/3"
        self.image_base_url = "https://image.tmdb.org/t/p/w500"
    
    async def search_movie(self, query: str) -> Optional[Dict]:
        """Search for a movie and return detailed information"""
        try:
            # Search for movies
            search_url = f"{self.base_url}/search/movie"
            search_params = {
                'api_key': self.api_key,
                'query': query,
                'language': 'en-US',
                'page': 1,
                'include_adult': False
            }
            
            response = requests.get(search_url, params=search_params)
            response.raise_for_status()
            
            search_data = response.json()
            
            if not search_data.get('results'):
                return None
            
            # Get the first (most relevant) result
            movie = search_data['results'][0]
            movie_id = movie['id']
            
            # Get detailed movie information
            details_url = f"{self.base_url}/movie/{movie_id}"
            details_params = {
                'api_key': self.api_key,
                'language': 'en-US',
                'append_to_response': 'credits,videos,similar'
            }
            
            details_response = requests.get(details_url, params=details_params)
            details_response.raise_for_status()
            
            details_data = details_response.json()
            
            # Format movie information
            movie_info = self._format_movie_data(details_data)
            
            return movie_info
            
        except requests.RequestException as e:
            logger.error(f"Error searching TMDB: {e}")
            raise Exception(f"Failed to search movies: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in movie search: {e}")
            raise Exception(f"Movie search failed: {str(e)}")
    
    def _format_movie_data(self, movie_data: Dict) -> Dict:
        """Format raw TMDB data into a clean structure"""
        try:
            # Basic information
            title = movie_data.get('title', 'Unknown Title')
            release_date = movie_data.get('release_date', '')
            year = release_date.split('-')[0] if release_date else 'Unknown'
            
            # Rating and runtime
            rating = movie_data.get('vote_average', 0)
            runtime = movie_data.get('runtime', 0)
            
            # Genres
            genres = [genre['name'] for genre in movie_data.get('genres', [])]
            
            # Overview
            overview = movie_data.get('overview', 'No overview available.')
            
            # Poster
            poster_path = movie_data.get('poster_path')
            poster_url = f"{self.image_base_url}{poster_path}" if poster_path else None
            
            # Cast (top 5)
            cast = []
            if 'credits' in movie_data and 'cast' in movie_data['credits']:
                cast = [
                    actor['name'] for actor in movie_data['credits']['cast'][:5]
                ]
            
            # Director
            director = "Unknown"
            if 'credits' in movie_data and 'crew' in movie_data['credits']:
                for crew_member in movie_data['credits']['crew']:
                    if crew_member.get('job') == 'Director':
                        director = crew_member['name']
                        break
            
            # Production companies
            production_companies = [
                company['name'] for company in movie_data.get('production_companies', [])[:3]
            ]
            
            # Budget and revenue
            budget = movie_data.get('budget', 0)
            revenue = movie_data.get('revenue', 0)
            
            return {
                'title': title,
                'year': year,
                'release_date': release_date or 'Unknown',
                'rating': round(rating, 1),
                'runtime': f"{runtime}" if runtime else "Unknown",
                'genres': genres,
                'overview': overview,
                'poster_url': poster_url,
                'cast': cast,
                'director': director,
                'production_companies': production_companies,
                'budget': self._format_currency(budget) if budget else "Unknown",
                'revenue': self._format_currency(revenue) if revenue else "Unknown",
                'popularity': round(movie_data.get('popularity', 0), 1),
                'vote_count': movie_data.get('vote_count', 0)
            }
            
        except Exception as e:
            logger.error(f"Error formatting movie data: {e}")
            return {
                'title': 'Error formatting movie data',
                'year': 'Unknown',
                'release_date': 'Unknown',
                'rating': 0,
                'runtime': 'Unknown',
                'genres': [],
                'overview': 'Unable to retrieve movie information.',
                'poster_url': None,
                'cast': [],
                'director': 'Unknown',
                'production_companies': [],
                'budget': 'Unknown',
                'revenue': 'Unknown',
                'popularity': 0,
                'vote_count': 0
            }
    
    def _format_currency(self, amount: int) -> str:
        """Format currency amounts"""
        if amount >= 1_000_000_000:
            return f"${amount / 1_000_000_000:.1f}B"
        elif amount >= 1_000_000:
            return f"${amount / 1_000_000:.1f}M"
        elif amount >= 1_000:
            return f"${amount / 1_000:.1f}K"
        else:
            return f"${amount:,}"
    
    async def get_trending_movies(self, time_window: str = 'week') -> List[Dict]:
        """Get trending movies"""
        try:
            url = f"{self.base_url}/trending/movie/{time_window}"
            params = {
                'api_key': self.api_key,
                'language': 'en-US'
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            movies = []
            
            for movie in data.get('results', [])[:10]:
                movies.append({
                    'title': movie.get('title', 'Unknown'),
                    'rating': round(movie.get('vote_average', 0), 1),
                    'release_date': movie.get('release_date', 'Unknown'),
                    'overview': movie.get('overview', '')[:100] + '...' if movie.get('overview') else '',
                    'poster_url': f"{self.image_base_url}{movie['poster_path']}" if movie.get('poster_path') else None
                })
            
            return movies
            
        except Exception as e:
            logger.error(f"Error getting trending movies: {e}")
            return []
