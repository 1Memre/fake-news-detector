import re

def validate_input(text: str) -> str | None:
    """
    Validates if the input text looks like a news article.
    Returns an error message if invalid, or None if valid.
    """
    text_clean = text.strip().lower()
    
    # Check 1: Greetings
    if re.match(r"^(hi|hello|hey|greetings|good morning|good evening)\b", text_clean):
        return "This appears to be a conversational greeting, not a news headline."

    # Check 2: Conversational Questions
    if re.match(r"^(how|what|who|why|when|where) (are|is|do|does|can|will) (you|i|we|it)\b", text_clean):
        return "This looks like a personal question or conversation, not a news article."

    # Check 3: Math patterns
    math_pattern = r"^\s*\d+\s*[\+\-\*\/=]\s*\d+"
    if re.search(math_pattern, text):
        return "This looks like a mathematical equation, not a news article."

    # Check 4: Gibberish / Random Characters
    consonants = len(re.findall(r"[bcdfghjklmnpqrstvwxyz]", text_clean))
    vowels = len(re.findall(r"[aeiou]", text_clean))
    # Heuristic: If vowels count is 0 and there are more than 3 consonants
    if vowels == 0 and consonants > 3:
         return "The text appears to be random characters or gibberish."
    
    # Check 5: Length (General fallback)
    if len(text.strip()) < 15:
        return "Input is too short to be a news article. Please enter a full headline or sentence."
        
    return None
