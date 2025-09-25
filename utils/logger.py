"""
Logging System
Centralized logging with colored output and multi-tab support
"""

import logging
import sys
from datetime import datetime
from typing import Optional
from PyQt6.QtCore import QObject, pyqtSignal

# Color codes for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for different log levels"""
    
    COLORS = {
        'DEBUG': Colors.CYAN,
        'INFO': Colors.GREEN,
        'WARNING': Colors.YELLOW,
        'ERROR': Colors.RED,
        'CRITICAL': Colors.PURPLE
    }
    
    def format(self, record):
        # Add color to level name
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{Colors.RESET}"
        
        # Add color to message
        if record.levelname.find('ERROR') >= 0:
            record.msg = f"{Colors.RED}{record.msg}{Colors.RESET}"
        elif record.levelname.find('WARNING') >= 0:
            record.msg = f"{Colors.YELLOW}{record.msg}{Colors.RESET}"
        elif record.levelname.find('INFO') >= 0:
            record.msg = f"{Colors.GREEN}{record.msg}{Colors.RESET}"
        
        return super().format(record)

class LogHandler(QObject):
    """Custom log handler for Qt integration"""
    
    # Signals for different log types
    ai_log_signal = pyqtSignal(str)
    network_log_signal = pyqtSignal(str)
    program_log_signal = pyqtSignal(str)
    all_log_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.log_buffer = []
    
    def emit_log(self, log_type: str, message: str, tokens: Optional[int] = None):
        """Emit log message to appropriate signal"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if tokens is not None:
            formatted_message = f"[{timestamp}] {message} (Tokens: {tokens})"
        else:
            formatted_message = f"[{timestamp}] {message}"
        
        # Emit to specific log type
        if log_type == "ai":
            self.ai_log_signal.emit(formatted_message)
        elif log_type == "network":
            self.network_log_signal.emit(formatted_message)
        elif log_type == "program":
            self.program_log_signal.emit(formatted_message)
        
        # Always emit to all logs
        self.all_log_signal.emit(formatted_message)
        
        # Store in buffer for file logging
        self.log_buffer.append(f"[{timestamp}] [{log_type.upper()}] {message}")

# Global log handler instance
_log_handler = LogHandler()

def setup_logging():
    """Setup application logging system"""
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    colored_formatter = ColoredFormatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(colored_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler
    try:
        file_handler = logging.FileHandler('conference_editor.log')
        file_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(file_handler)
    except Exception as e:
        print(f"Warning: Could not create log file: {e}")

def get_ai_logger():
    """Get logger for AI operations"""
    return logging.getLogger('ai')

def get_network_logger():
    """Get logger for network operations"""
    return logging.getLogger('network')

def get_processing_logger():
    """Get logger for document processing"""
    return logging.getLogger('processing')

def get_program_logger():
    """Get logger for general program operations"""
    return logging.getLogger('program')

def log_ai_message(message: str, tokens: Optional[int] = None):
    """Log AI-specific message"""
    _log_handler.emit_log("ai", message, tokens)

def log_network_message(message: str):
    """Log network-specific message"""
    _log_handler.emit_log("network", message)

def log_program_message(message: str):
    """Log program-specific message"""
    _log_handler.emit_log("program", message)

def get_log_handler():
    """Get global log handler instance"""
    return _log_handler

# Initialize logging on import
setup_logging()