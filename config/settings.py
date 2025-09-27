"""
Application Settings
Global configuration and default values
"""

import os
from pathlib import Path

# Application Information
APP_NAME = "Conference Editing Assistant"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Conference Editor Team"

# Default Settings
DEFAULT_PROMPT = """Fix only spelling and dictation errors in the following text. 
Maintain the exact meaning, structure, and style. 
Do not improve grammar, clarity, or flow. 
Do not add, remove, or restructure content.
Return only the corrected text:"""

# API Configuration
API_TIMEOUT = 15  # seconds
API_RATE_LIMIT_DELAY = 3  # seconds between requests
API_MAX_RETRIES = 3

# File Configuration
OUTPUT_FILE_SUFFIX_CLEAN = "_Edited_Clean"
OUTPUT_FILE_SUFFIX_HIGHLIGHTED = "_Edited_Highlighted"
DEFAULT_OUTPUT_FORMAT = "docx"

# Directory Configuration
APP_DATA_DIR = Path.home() / ".CYSP-proofreader"
LOGS_DIR = APP_DATA_DIR / "logs"

# Network Configuration
API_BASE_URL = "https://openrouter.ai/api/v1"

# UI Configuration
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PROGRESS_UPDATE_INTERVAL = 100  # milliseconds

def ensure_app_directories():
    """Ensure application directories exist"""
    APP_DATA_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)

def get_app_data_dir():
    """Get application data directory"""
    return APP_DATA_DIR

def get_logs_dir():
    """Get logs directory"""
    return LOGS_DIR

# Initialize directories on import
ensure_app_directories()