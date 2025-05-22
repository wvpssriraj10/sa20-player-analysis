import os
import json
import logging
import requests
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SA20DataFetcher:
    def __init__(self, api_key: str):
        """Initialize the SA20 data fetcher with API key."""
        self.api_key = api_key
        self.base_url = "https://api.cricapi.com/v1"
        self.headers = {
            "apikey": self.api_key,
            "Content-Type": "application/json"
        }
        
    def fetch_matches(self, series_id: str = "c75f8952-74d4-416f-b7b4-7da4b4e3ae6e") -> List[Dict]:
        """
        Fetch all SA20 matches for the given series ID.
        
        Args:
            series_id: The ID of the SA20 series (default is 2024 season)
            
        Returns:
            List of match data dictionaries
        """
        try:
            url = f"{self.base_url}/matches"
            params = {
                "series_id": series_id,
                "offset": 0
            }
            
            all_matches = []
            while True:
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                data = response.json()
                
                if not data.get("data"):
                    break
                    
                all_matches.extend(data["data"])
                
                if not data.get("pagination", {}).get("next"):
                    break
                    
                params["offset"] += 20  # API pagination size
                
            logger.info(f"Successfully fetched {len(all_matches)} matches")
            return all_matches
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching matches: {str(e)}")
            raise
            
    def fetch_match_details(self, match_id: str) -> Dict:
        """
        Fetch detailed information for a specific match.
        
        Args:
            match_id: The ID of the match to fetch
            
        Returns:
            Dictionary containing match details
        """
        try:
            url = f"{self.base_url}/match_info"
            params = {"id": match_id}
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data.get("data"):
                raise ValueError(f"No data found for match ID: {match_id}")
                
            return data["data"][0]
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching match details for {match_id}: {str(e)}")
            raise
            
    def save_data(self, data: Dict, filename: str) -> None:
        """
        Save the fetched data to a JSON file.
        
        Args:
            data: The data to save
            filename: The name of the file to save to
        """
        try:
            output_dir = Path("data/raw")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            filepath = output_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
                
            logger.info(f"Data saved to {filepath}")
            
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
            raise

def main():
    """Main function to fetch and save SA20 data."""
    try:
        # Get API key from environment variable
        api_key = os.getenv("CRICAPI_KEY")
        if not api_key:
            raise ValueError("CRICAPI_KEY environment variable not set")
            
        # Initialize fetcher
        fetcher = SA20DataFetcher(api_key)
        
        # Fetch all matches
        matches = fetcher.fetch_matches()
        
        # Save matches data
        fetcher.save_data(
            {"matches": matches},
            f"sa20_matches_{datetime.now().strftime('%Y%m%d')}.json"
        )
        
        # Fetch and save detailed match data
        for match in matches:
            match_id = match["id"]
            match_details = fetcher.fetch_match_details(match_id)
            fetcher.save_data(
                match_details,
                f"match_{match_id}.json"
            )
            
        logger.info("Data collection completed successfully")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main() 