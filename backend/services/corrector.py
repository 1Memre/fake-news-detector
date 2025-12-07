from textblob import TextBlob, Word
import logging
import re

logger = logging.getLogger(__name__)

# Common proper nouns and terms that should NOT be corrected
PRESERVE_WORDS = {
    # Political figures (common in news)
    'biden', 'trump', 'obama', 'clinton', 'harris', 'pence', 'pelosi', 'mcconnell',
    'putin', 'zelensky', 'xi', 'modi', 'macron', 'trudeau', 'netanyahu',
    
    # Political terms
    'bipartisan', 'democrat', 'republican', 'senate', 'congress', 'parliament',
    'legislation', 'referendum', 'caucus', 'filibuster',
    
    # Common news terms
    'covid', 'pandemic', 'vaccine', 'brexit', 'nato', 'un', 'eu', 'gdp',
    'cryptocurrency', 'bitcoin', 'ai', 'tech', 'startup',
    
    # Common abbreviations
    'usa', 'uk', 'uae', 'ceo', 'cfo', 'fbi', 'cia', 'nasa', 'who'
}

def correct_text(text: str) -> str:
    """
    Corrects spelling mistakes in the text using TextBlob with smart filtering.
    Only corrects actual typos, preserves proper nouns and valid words.
    Returns the corrected text.
    """
    try:
        # Split into words while preserving punctuation
        words = re.findall(r'\b\w+\b|[^\w\s]', text)
        corrected_words = []
        changed = False
        
        for word in words:
            # Skip punctuation
            if not word.isalnum():
                corrected_words.append(word)
                continue
                
            # Skip if it's a preserved word (case-insensitive)
            if word.lower() in PRESERVE_WORDS:
                corrected_words.append(word)
                continue
            
            # Skip if word is capitalized (likely a proper noun)
            if word[0].isupper() and len(word) > 1:
                corrected_words.append(word)
                continue
            
            # Skip short words (likely acronyms or valid short words)
            if len(word) <= 2:
                corrected_words.append(word)
                continue
            
            # Try to correct the word
            try:
                word_obj = Word(word)
                corrected = str(word_obj.correct())
                
                # Only use correction if it's different AND the original word
                # seems like a typo (not in common dictionary)
                if corrected != word and corrected.lower() != word.lower():
                    # Additional check: only correct if confidence is high
                    # (the correction is a real word and original isn't)
                    try:
                        # Check if original word exists in dictionary
                        original_valid = len(word_obj.spellcheck()) > 0 and word_obj.spellcheck()[0][1] > 0.5
                        if not original_valid:
                            corrected_words.append(corrected)
                            changed = True
                            logger.info(f"Corrected: '{word}' -> '{corrected}'")
                        else:
                            corrected_words.append(word)
                    except:
                        corrected_words.append(word)
                else:
                    corrected_words.append(word)
            except:
                corrected_words.append(word)
        
        # Reconstruct text
        result = ' '.join(corrected_words)
        # Fix spacing around punctuation
        result = re.sub(r'\s+([.,!?;:])', r'\1', result)
        result = re.sub(r'([.,!?;:])\s*', r'\1 ', result)
        result = result.strip()
        
        if changed:
            logger.info(f"Auto-correction applied: '{text[:50]}...' -> '{result[:50]}...'")
        
        return result
    except Exception as e:
        logger.error(f"Error in auto-correction: {e}")
        return text

