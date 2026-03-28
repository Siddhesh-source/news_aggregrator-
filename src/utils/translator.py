"""
Sarvam AI Translation Service
Handles translation of content to Indian languages using Sarvam API
"""

import os
import requests
import logging
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
SARVAM_API_URL = "https://api.sarvam.ai/translate"

# Language code mapping
LANGUAGE_CODES = {
    'en': 'en-IN',
    'hi': 'hi-IN',
    'ta': 'ta-IN',
    'te': 'te-IN',
    'bn': 'bn-IN',
    'mr': 'mr-IN',
    'gu': 'gu-IN',
    'kn': 'kn-IN',
    'ml': 'ml-IN',
    'pa': 'pa-IN',
    'or': 'or-IN',
    'as': 'as-IN'
}


def translate_text(text: str, target_language: str, source_language: str = 'en') -> str:
    """
    Translate text using Sarvam AI API
    
    Args:
        text: Text to translate
        target_language: Target language code (e.g., 'hi', 'ta')
        source_language: Source language code (default: 'en')
    
    Returns:
        Translated text
    """
    if not SARVAM_API_KEY:
        logger.warning("Sarvam API key not found, returning original text")
        return text
    
    # If target is same as source, return original
    if target_language == source_language:
        return text
    
    # Get Sarvam language codes
    source_lang = LANGUAGE_CODES.get(source_language, 'en-IN')
    target_lang = LANGUAGE_CODES.get(target_language, 'hi-IN')
    
    try:
        headers = {
            'API-Subscription-Key': SARVAM_API_KEY,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'input': text,
            'source_language_code': source_lang,
            'target_language_code': target_lang,
            'speaker_gender': 'Male',
            'mode': 'formal',
            'model': 'mayura:v1',
            'enable_preprocessing': True
        }
        
        response = requests.post(SARVAM_API_URL, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            translated_text = result.get('translated_text', text)
            logger.info(f"Successfully translated text to {target_language}")
            return translated_text
        else:
            logger.error(f"Sarvam API error: {response.status_code} - {response.text}")
            return text
            
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        return text


def translate_article(article: Dict, target_language: str) -> Dict:
    """
    Translate article content to target language
    
    Args:
        article: Article dictionary with title, summary, exam_angle, etc.
        target_language: Target language code
    
    Returns:
        Translated article dictionary
    """
    if target_language == 'en':
        return article
    
    translated = article.copy()
    
    # Translate key fields
    if 'title' in article and article['title']:
        translated['title'] = translate_text(article['title'], target_language)
    
    if 'summary' in article and article['summary']:
        translated['summary'] = translate_text(article['summary'], target_language)
    
    if 'exam_angle' in article and article['exam_angle']:
        translated['exam_angle'] = translate_text(article['exam_angle'], target_language)
    
    if 'key_points' in article and isinstance(article['key_points'], list):
        translated['key_points'] = [
            translate_text(point, target_language) for point in article['key_points']
        ]
    
    return translated


def translate_mcq(mcq: Dict, target_language: str) -> Dict:
    """
    Translate MCQ content to target language
    
    Args:
        mcq: MCQ dictionary with question, options, explanation, etc.
        target_language: Target language code
    
    Returns:
        Translated MCQ dictionary
    """
    if target_language == 'en':
        return mcq
    
    translated = mcq.copy()
    
    # Translate question
    if 'question' in mcq and mcq['question']:
        translated['question'] = translate_text(mcq['question'], target_language)
    
    # Translate options
    for option_key in ['option_a', 'option_b', 'option_c', 'option_d']:
        if option_key in mcq and mcq[option_key]:
            translated[option_key] = translate_text(mcq[option_key], target_language)
    
    # Translate explanation
    if 'explanation' in mcq and mcq['explanation']:
        translated['explanation'] = translate_text(mcq['explanation'], target_language)
    
    # Translate learning insight
    if 'learning_insight' in mcq and mcq['learning_insight']:
        translated['learning_insight'] = translate_text(mcq['learning_insight'], target_language)
    
    return translated


def translate_batch(texts: List[str], target_language: str, source_language: str = 'en') -> List[str]:
    """
    Translate multiple texts (batch processing)
    
    Args:
        texts: List of texts to translate
        target_language: Target language code
        source_language: Source language code
    
    Returns:
        List of translated texts
    """
    if target_language == source_language:
        return texts
    
    translated_texts = []
    for text in texts:
        translated = translate_text(text, target_language, source_language)
        translated_texts.append(translated)
    
    return translated_texts


def get_supported_languages() -> List[Dict[str, str]]:
    """
    Get list of supported languages
    
    Returns:
        List of language dictionaries with code and name
    """
    return [
        {'code': 'en', 'name': 'English', 'native_name': 'English'},
        {'code': 'hi', 'name': 'Hindi', 'native_name': 'हिन्दी'},
        {'code': 'ta', 'name': 'Tamil', 'native_name': 'தமிழ்'},
        {'code': 'te', 'name': 'Telugu', 'native_name': 'తెలుగు'},
        {'code': 'bn', 'name': 'Bengali', 'native_name': 'বাংলা'},
        {'code': 'mr', 'name': 'Marathi', 'native_name': 'मराठी'},
        {'code': 'gu', 'name': 'Gujarati', 'native_name': 'ગુજરાતી'},
        {'code': 'kn', 'name': 'Kannada', 'native_name': 'ಕನ್ನಡ'},
        {'code': 'ml', 'name': 'Malayalam', 'native_name': 'മലയാളം'},
        {'code': 'pa', 'name': 'Punjabi', 'native_name': 'ਪੰਜਾਬੀ'},
        {'code': 'or', 'name': 'Odia', 'native_name': 'ଓଡ଼ିଆ'},
        {'code': 'as', 'name': 'Assamese', 'native_name': 'অসমীয়া'}
    ]
