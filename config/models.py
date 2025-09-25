"""
AI Model Configuration
Centralized model definitions with token limits and display names
"""

# Default recommended models for easy selection
RECOMMENDED_MODELS = {
    "deepseek/deepseek-chat-v3.1:free": {
        "max_tokens": 128000,
        "display_name": "DeepSeek v3.1 Free",
        "provider": "DeepSeek"
    },
    "microsoft/phi-3-mini-128k-instruct:free": {
        "max_tokens": 128000,
        "display_name": "Phi-3 Mini Free",
        "provider": "Microsoft"
    },
    "google/gemma-7b-it:free": {
        "max_tokens": 8192,
        "display_name": "Gemma 7B IT Free",
        "provider": "Google"
    },
    "mistralai/mistral-7b-instruct:free": {
        "max_tokens": 32768,
        "display_name": "Mistral 7B Free",
        "provider": "Mistral"
    }
}

# Default model for first-time use
DEFAULT_MODEL = "deepseek/deepseek-chat-v3.1:free"

def get_model_config(model_name):
    """Get configuration for a specific model, with fallback to default values"""
    if model_name in RECOMMENDED_MODELS:
        return RECOMMENDED_MODELS[model_name]
    else:
        # Return default config for custom models
        return {
            "max_tokens": 128000,  # Conservative default
            "display_name": model_name,
            "provider": "Custom"
        }

def get_available_models():
    """Get list of available models for dropdown"""
    return [(name, config["display_name"]) for name, config in RECOMMENDED_MODELS.items()]

def get_model_max_tokens(model_name):
    """Get maximum tokens for a model"""
    config = get_model_config(model_name)
    return config.get("max_tokens", 128000)

def is_model_available(model_name):
    """Check if model is in recommended list (for validation)"""
    return model_name in RECOMMENDED_MODELS