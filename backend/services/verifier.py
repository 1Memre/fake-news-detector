from duckduckgo_search import DDGS
import logging
import asyncio
from typing import List, Dict, Optional
from async_lru import alru_cache

logger = logging.getLogger(__name__)

# List of trusted news domains
TRUSTED_DOMAINS = [
    "bbc.com", "reuters.com", "cnn.com", "nytimes.com", "washingtonpost.com",
    "theguardian.com", "apnews.com", "npr.org", "bloomberg.com", "wsj.com",
    "nbcnews.com", "abcnews.go.com", "cbsnews.com", "usatoday.com", "time.com",
    "forbes.com", "economist.com", "ft.com", "snopes.com", "politifact.com",
    "wikipedia.org", "britannica.com", "nationalgeographic.com", "history.com",
    "science.org", "nature.com", "nasa.gov", "who.int", "cdc.gov"
]

# Sensationalist / Clickbait Keywords
CLICKBAIT_KEYWORDS = [
    "shocking", "secret", "banned", "censored", "miracle", "you won't believe",
    "mind-blowing", "exposed", "hidden truth", "conspiracy", "illuminati",
    "deep state", "hoax", "fake news", "mainstream media lies", "viral",
    "destroy", "obliterate", "shreds", "bombshell"
]

def _search_sync(query: str, max_results: int = 10):
    with DDGS() as ddgs:
        return list(ddgs.text(query, max_results=max_results))

@alru_cache(maxsize=128)
async def verify_sources(text: str) -> List[Dict[str, str]]:
    """
    Searches DuckDuckGo for the text and checks if results match trusted domains.
    """
    try:
        # Use the first 100 characters as the query
        query = text[:100]
        logger.info(f"Searching for: {query}")
        
        found_sources = []
        
        # Run sync search in thread
        results = await asyncio.to_thread(_search_sync, query, 10)
            
        if not results:
            return []

        for result in results:
            url = result.get('href', '')
            title = result.get('title', '')
            
            for domain in TRUSTED_DOMAINS:
                if domain in url:
                    logger.info(f"MATCH: {domain} in {url}")
                    found_sources.append({"domain": domain, "url": url, "title": title})
                    break 
            
            if len(found_sources) >= 3:
                break
                
        return found_sources
    except Exception as e:
        logger.error(f"Search error: {e}")
        return []

@alru_cache(maxsize=64)
async def get_correction(text: str) -> Optional[Dict[str, str]]:
    """
    Searches for related stories from trusted sources to provide context/correction.
    """
    try:
        stop_words = {"the", "is", "at", "which", "on", "a", "an", "and", "or", "but", "in", "with", "to", "of", "for", "by", "secret", "shocking", "revealed", "banned", "yesterday", "today"}
        words = text.lower().split()
        keywords = [w for w in words if w not in stop_words and len(w) > 3]
        
        query = f"{' '.join(keywords[:5])} fact check"
        logger.info(f"Correction Search Query: {query}")
        
        # Run sync search in thread
        results = await asyncio.to_thread(_search_sync, query, 10)
            
        if results:
            for result in results:
                url = result.get('href', '')
                title = result.get('title', '')
                
                for domain in TRUSTED_DOMAINS:
                    if domain in url:
                        logger.info(f"FOUND CORRECTION: {title} from {domain}")
                        return {"domain": domain, "url": url, "title": title}
        return None
    except Exception as e:
        logger.error(f"Correction search error: {e}")
        return None

def generate_explanation(text: str, prediction: str, sources: list) -> str:
    """
    Generates a human-readable explanation for the prediction.
    """
    if prediction == "REAL":
        if sources:
            return f"This news is verified by {len(sources)} trusted source(s) including {sources[0]['domain']}."
        else:
            return "The language patterns and writing style match those typically found in credible news reporting."
    
    else: # FAKE
        reasons = []
        
        # Reason 1: No sources
        if not sources:
            reasons.append("We could not find this specific story on any of our trusted news sources.")
            
        # Reason 2: Keywords
        found_keywords = [word for word in CLICKBAIT_KEYWORDS if word in text.lower()]
        if found_keywords:
            reasons.append(f"The text contains sensationalist or clickbait language: '{', '.join(found_keywords[:3])}'.")
            
        if not reasons:
            return "The content matches patterns often associated with misinformation or unreliable news sources."
            
        return " ".join(reasons)
