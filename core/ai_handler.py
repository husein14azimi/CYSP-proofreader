"""
AI Handler
Manages OpenRouter API integration and AI processing
"""

import logging
import time
import requests
import tiktoken
from typing import Optional, Dict, Callable
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
            "HTTP-Referer": "https://cysp2025.ut.ac.ir",
            "X-Title": "CYSP Proofreader"
        })
        
    def process_text(self, text: str, model_name: str) -> Optional[str]:
        """Process text through AI model (wrapper for status version)"""
        return self.process_text_with_status(text, model_name, None)
    
    def process_text_with_status(self, text: str, model_name: str, status_callback: Optional[Callable[[str], None]] = None) -> Optional[str]:
        """
        Process text through AI model with status updates
        
        Args:
            text: Text to process
            model_name: Full OpenRouter model name
            status_callback: Function to call with status updates
            
        Returns:
            Processed text or None if failed
        """
        if not self.api_key:
            self.logger.error("[AI Handler] API key not set")
            return None
            
        if not model_name:
            self.logger.error("[AI Handler] Model name not provided")
            return None
            
        for attempt in range(API_MAX_RETRIES):
            try:
                # Rate limiting
                self._enforce_rate_limit()
                
                prompt = self._get_system_prompt()
                
                # Calculate ETA based on provided metrics
                token_count = self.count_tokens(text, model_name)
                if status_callback:
                    estimated_time = self._calculate_eta(token_count)
                    connection_quality = self._assess_connection_quality()
                    status_callback(
                        f"Sending {token_count} tokens to {model_name}... | "
                        f"ETA: ~{estimated_time}s | Connection Quality: {connection_quality}"
                    )
                
                response = self._send_request_with_status(prompt, text, model_name, status_callback)
                
                if response:
                    tokens_sent = self.count_tokens(text, model_name)
                    tokens_received = self.count_tokens(response, model_name)
                    log_ai_message(f"AI processing successful. Model: {model_name}, Tokens sent: {tokens_sent}, received: {tokens_received}", tokens_sent)
                    if status_callback:
                        status_callback(f"Received {tokens_received} tokens from {model_name}")
                    return response
                else:
                    self.logger.warning(f"[AI Handler] AI processing attempt {attempt + 1} failed for model {model_name}")
                    if status_callback:
                        status_callback(f"AI processing attempt {attempt + 1} failed, retrying...")
                    
            except Exception as e:
                self.logger.error(f"[AI Handler] AI processing error (attempt {attempt + 1}): {str(e)}")
                if status_callback:
                    status_callback(f"Error: {str(e)}, attempt {attempt + 1}/{API_MAX_RETRIES}")
                
            if attempt < API_MAX_RETRIES - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                
        return None
    
    def _send_request_with_status(self, system_prompt: str, user_text: str, model_name: str, status_callback: Optional[Callable[[str], None]]) -> Optional[str]:
        """Send request to OpenRouter API with status updates"""
        # Clean URL without trailing spaces
        api_url = "https://openrouter.ai/api/v1/chat/completions"
        
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ]
        }
        
        try:
            start_time = time.time()
            if status_callback:
                status_callback(f"Waiting for first token from {model_name} (3s avg)...")
            
            response = self.session.post(
                api_url,
                json=payload,
                timeout=API_TIMEOUT
            )
            response.raise_for_status()
            
            total_time = time.time() - start_time
            data = response.json()
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]
                
                # Update status with actual performance
                tokens_received = self.count_tokens(content, model_name)
                throughput = tokens_received / total_time if total_time > 0 else 0
                connection_quality = self._assess_connection_quality()
                
                if status_callback:
                    status_callback(
                        f"Received response: {tokens_received} tokens in {total_time:.1f}s "
                        f"({throughput:.1f} tok/s) | Connection Quality: {connection_quality}"
                    )
                
                log_ai_message(f"API response received for model {model_name}", tokens_received)
                return content
            else:
                self.logger.error(f"[AI Handler] Invalid API response format: {data}")
                return None
                
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"[AI Handler] HTTP Error: {str(e)} - Status Code: {response.status_code}")
            
            # Show the actual response content for debugging
            try:
                error_content = response.text
                self.logger.error(f"[AI Handler] Error response content: {error_content}")
            except:
                self.logger.error(f"[AI Handler] Could not read error response content")
            
            return None
        except requests.exceptions.RequestException as e:
            self.logger.error(f"[AI Handler] Request failed: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"[AI Handler] API response parsing failed: {str(e)}")
            return None
    
    def _calculate_eta(self, token_count: int) -> int:
        """
        Calculate ETA based on provided metrics:
        - First token latency: 3 seconds
        - Generation throughput: 10 tokens per second
        - Pessimistic estimate (1.5x multiplier)
        """
        base_time = 3 + (token_count / 10)  # 3s + (tokens / 10 tok/s)
        pessimistic_time = int(base_time * 1.5)  # Pessimistic estimate
        return pessimistic_time
    
    def _assess_connection_quality(self) -> str:
        """Assess connection quality based on recent performance"""
        # This is a simplified assessment - in a real app, you'd track actual response times
        # For now, return a placeholder that could be enhanced with actual metrics
        return "Fair"  # Placeholder - could be "Good", "Fair", "Slow" based on actual performance
    
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
            self.logger.warning("[AI Handler] Model name is None, using estimate")
            return len(text) // 3
            
        try:
            # Use tiktoken for token counting - use explicit encoding method
            encoding_name = self._get_encoding_for_model(model_name)
            try:
                encoding = tiktoken.encoding_for_model(encoding_name)
            except KeyError:
                # If specific encoding fails, use cl100k_base as default
                encoding = tiktoken.get_encoding("cl100k_base")
            
            token_count = len(encoding.encode(text))
            return token_count
        except Exception as e:
            self.logger.warning(f"[AI Handler] Token counting failed, using estimate: {str(e)}")
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