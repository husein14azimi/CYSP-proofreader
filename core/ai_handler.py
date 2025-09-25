"""
AI Handler
Manages OpenRouter API integration and AI processing
"""

import logging
import time
import requests
import tiktoken
from typing import Optional, Dict
from config.models import get_model_max_tokens as config_get_model_max_tokens  # Import from config
from config.settings import API_BASE_URL, API_TIMEOUT, API_RATE_LIMIT_DELAY, API_MAX_RETRIES
from utils.logger import get_ai_logger, log_ai_message

class AIHandler:
    """Handles AI model interactions via OpenRouter API"""
    
    def __init__(self):
        self.logger = get_ai_logger()
        self.api_key = None
        self.session = requests.Session()
        self.last_request_time = 0
        
    def set_api_key(self, api_key: str):
        """Set API key for authentication"""
        self.api_key = api_key
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://conference-editor.local",
            "X-Title": "Conference Editing Assistant"
        })
        
    def process_text(self, text: str, model_name: str) -> Optional[str]:
        """
        Process text through AI model
        
        Args:
            text: Text to process
            model_name: Full OpenRouter model name (e.g., "deepseek/deepseek-chat-v3.1:free")
            
        Returns:
            Processed text or None if failed
        """
        if not self.api_key:
            self.logger.error("API key not set")
            return None
            
        if not model_name:
            self.logger.error("Model name not provided")
            return None
            
        for attempt in range(API_MAX_RETRIES):
            try:
                # Rate limiting
                self._enforce_rate_limit()
                
                prompt = self._get_system_prompt()
                response = self._send_request(prompt, text, model_name)
                
                if response:
                    tokens_sent = self.count_tokens(text, model_name)
                    log_ai_message(f"AI processing successful. Model: {model_name}, Tokens: {tokens_sent}", tokens_sent)
                    return response
                else:
                    self.logger.warning(f"AI processing attempt {attempt + 1} failed for model {model_name}")
                    
            except Exception as e:
                self.logger.error(f"AI processing error (attempt {attempt + 1}): {str(e)}")
                
            if attempt < API_MAX_RETRIES - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                
        return None
    
    def _send_request(self, system_prompt: str, user_text: str, model_name: str) -> Optional[str]:
        """Send request to OpenRouter API"""
        # Fixed URL - removed trailing space
        url = f"{API_BASE_URL}/chat/completions"
        
        payload = {
            "model": model_name,  # Use the full model name provided by user
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}  # This is where the document content goes
            ]
        }
        
        try:
            self.logger.info(f"Sending request to {url} with model {model_name}")
            response = self.session.post(
                url, 
                json=payload,  # This includes the document content in the user message
                timeout=API_TIMEOUT
            )
            response.raise_for_status()
            
            data = response.json()
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]
                log_ai_message(f"API response received for model {model_name}", self.count_tokens(content, model_name))
                return content
            else:
                self.logger.error(f"Invalid API response format: {data}")
                return None
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"API response parsing failed: {str(e)}")
            return None
    
    def _enforce_rate_limit(self):
        """Enforce rate limiting between requests"""
        elapsed = time.time() - self.last_request_time
        if elapsed < API_RATE_LIMIT_DELAY:
            sleep_time = API_RATE_LIMIT_DELAY - elapsed
            time.sleep(sleep_time)
        self.last_request_time = time.time()
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for dictation correction"""
        return """Fix only spelling and dictation errors in the following text. 
Maintain the exact meaning, structure, and style. 
Do not improve grammar, clarity, or flow. 
Do not add, remove, or restructure content.
Return only the corrected text:"""
    
    def count_tokens(self, text: str, model_name: str) -> int:
        """Count tokens in text for given model"""
        if not model_name:  # Handle the case where model_name is None
            self.logger.warning("Model name is None, using estimate")
            return len(text) // 3
            
        try:
            # Use tiktoken for token counting
            encoding_name = self._get_encoding_for_model(model_name)
            encoding = tiktoken.encoding_for_model(encoding_name)
            token_count = len(encoding.encode(text))
            return token_count
        except Exception as e:
            self.logger.warning(f"Token counting failed, using estimate: {str(e)}")
            # Rough estimate: 1 token ≈ 3-4 characters
            return len(text) // 3
    
    def _get_encoding_for_model(self, model_name: str) -> str:
        """Map model names to appropriate token encodings"""
        if not model_name:  # Handle the case where model_name is None
            return "cl100k_base"
            
        # Extract base model name for encoding lookup
        base_model = model_name.split(':')[0].split('/')[-1].lower()
        
        model_mapping = {
            "gpt-3.5": "gpt-3.5-turbo",
            "gpt-4": "gpt-4",
            "claude": "cl100k_base",
            "deepseek": "cl100k_base",
            "mistral": "cl100k_base",
            "llama": "cl100k_base",
            "mixtral": "cl100k_base",
            "phi": "cl100k_base"
        }
        
        for key, encoding in model_mapping.items():
            if key in base_model:
                return encoding
        return "cl100k_base"  # Default
    
    def get_model_max_tokens(self, model_name: str) -> int:
        """Get maximum tokens for model from config"""
        if not model_name:  # Handle the case where model_name is None
            return 128000  # Default
        return config_get_model_max_tokens(model_name)

# Convenience function
def create_ai_handler() -> AIHandler:
    """Factory function to create AI handler"""
    return AIHandler()