"""
Main Window
Primary application interface with tabbed layout
"""

import sys
import logging
from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QVBoxLayout, 
                            QWidget, QStatusBar, QLabel, QApplication)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import os
import sys
from config.settings import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT
from config.models import DEFAULT_MODEL
from ui.tabs.file_tab import FileTab
from ui.tabs.api_tab import APITab
from ui.tabs.prompt_tab import PromptTab
from ui.tabs.logs_tab import LogsTab
from core.document_processor import DocumentProcessor
from core.ai_handler import AIHandler
from core.file_manager import FileManager
from utils.logger import get_log_handler

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class MainWindow(QMainWindow):
    """Main application window with tabbed interface"""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.init_core_components()
        self.init_ui()
        self.setup_connections()
        self.set_initial_model()
        self.logger.info("Main window initialized")
    
    def init_core_components(self):
        """Initialize core application components"""
        self.document_processor = DocumentProcessor()
        self.ai_handler = AIHandler()
        self.file_manager = FileManager()
        
        # Connect components
        self.document_processor.set_ai_handler(self.ai_handler)
    
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle(f"{APP_NAME}")
        
        # Set window icon - this will show in title bar and taskbar
        try:
            icon_path = get_resource_path("ui/resources/icon.ico")
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
            else:
                # Fallback to default icon if not found
                self.logger.warning(f"Icon file not found: {icon_path}")
        except Exception as e:
            self.logger.error(f"Failed to set window icon: {e}")
        
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(600, 400)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Create tabs
        self.create_tabs()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.progress_label = QLabel("Ready")
        self.status_bar.addPermanentWidget(self.progress_label)
        
        # Set initial tab
        self.tab_widget.setCurrentIndex(0)
    
    def create_tabs(self):
        """Create and add all tabs to the interface"""
        # File Selection Tab
        self.file_tab = FileTab(self.file_manager, self.document_processor)
        self.tab_widget.addTab(self.file_tab, "File Selection")
        
        # API Configuration Tab
        self.api_tab = APITab(self.ai_handler)
        self.tab_widget.addTab(self.api_tab, "API Configuration")
        
        # Prompt Customization Tab
        self.prompt_tab = PromptTab()
        self.tab_widget.addTab(self.prompt_tab, "Prompt Customization")
        
        # Processing Logs Tab
        self.logs_tab = LogsTab()
        self.tab_widget.addTab(self.logs_tab, "Processing Logs")
    
    def setup_connections(self):
        """Setup signal-slot connections"""
        # Connect file tab signals
        self.file_tab.process_started.connect(self.on_process_started)
        self.file_tab.process_completed.connect(self.on_process_completed)
        self.file_tab.process_error.connect(self.on_process_error)
        
        # Connect API tab signals
        self.api_tab.api_key_changed.connect(self.on_api_key_changed)
        self.api_tab.model_changed.connect(self.on_model_changed)
        
        # Connect log handler signals
        log_handler = get_log_handler()
        log_handler.ai_log_signal.connect(self.logs_tab.add_ai_log)
        log_handler.network_log_signal.connect(self.logs_tab.add_network_log)
        log_handler.program_log_signal.connect(self.logs_tab.add_program_log)
        log_handler.all_log_signal.connect(self.logs_tab.add_all_log)
    
    def set_initial_model(self):
        """Set the initial model when application starts"""
        # Set default model in document processor
        self.document_processor.set_model(DEFAULT_MODEL)
        self.logger.info(f"Initial model set to: {DEFAULT_MODEL}")
    
    def on_process_started(self):
        """Handle process started event"""
        self.progress_label.setText("Processing document...")
        self.tab_widget.setTabEnabled(0, False)  # Disable file tab during processing
        self.status_bar.showMessage("Document processing started", 3000)
        # Don't change tab - stay on file tab
    
    def on_process_completed(self, message: str):
        """Handle process completed event"""
        self.progress_label.setText("Ready")
        self.tab_widget.setTabEnabled(0, True)  # Re-enable file tab
        self.status_bar.showMessage(f"Processing completed: {message}", 5000)
    
    def on_process_error(self, error_message: str):
        """Handle process error event"""
        self.progress_label.setText("Error occurred")
        self.progress_label.setStyleSheet("color: red;")
        self.tab_widget.setTabEnabled(0, True)  # Re-enable file tab
        self.status_bar.showMessage(f"Error: {error_message}", 10000)
        
        # Reset color after delay
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(3000, lambda: self.progress_label.setStyleSheet(""))
    
    def on_api_key_changed(self, api_key: str):
        """Handle API key change"""
        self.logger.info("API key updated")
        self.status_bar.showMessage("API key configured", 2000)
    
    def on_model_changed(self, model_name: str):
        """Handle model change"""
        self.document_processor.set_model(model_name)  # This sets the model in document processor
        self.logger.info(f"Model changed to: {model_name}")
        self.status_bar.showMessage(f"Model set to: {model_name}", 2000)
    
    def closeEvent(self, event):
        """Handle application close event"""
        self.logger.info("Application closing")
        event.accept()

# Factory function
def create_main_window() -> MainWindow:
    """Factory function to create main window"""
    return MainWindow()