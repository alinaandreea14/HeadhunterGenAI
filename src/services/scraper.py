# ==============================================================================
# UTILS - SCRAPER (Data Collection)
# ==============================================================================

import re
import requests
from bs4 import BeautifulSoup

def scrape_clean_job_text(url: str, max_chars: int = 3000) -> str:
    """
    It downloads the page and returns clean text, optimized for the LLM context.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return f"Error: Status code {response.status_code}"
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove unnecessary elements that consume tokens.
        for junk in soup(["script", "style", "nav", "footer", "header", "aside", "iframe"]):
            junk.decompose()
            
        # Extract the text and remove the multiple spaces
        text = soup.get_text(separator=' ', strip=True)
        text = re.sub(r'\s+', ' ', text)
        
        return text[:max_chars] 
        
    except Exception as e:
        return f"Scraping Error: {str(e)}"