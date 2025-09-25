#!/usr/bin/env python3
"""
Conference Editing Assistant
Desktop application for AI-powered dictation/spelling correction
"""

import sys
import logging
import traceback
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

def setup_logging():
    """Configure application logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('conference_editor.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """Application entry point"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("Conference Editing Assistant")
        app.setApplicationVersion("1.0.0")
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        logger.info("Conference Editing Assistant started successfully")
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    main()