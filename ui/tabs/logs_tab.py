"""
Processing Logs Tab
Displays various types of application logs in separate tabs
"""

import logging
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QTextEdit,
                            QHBoxLayout, QPushButton, QLabel)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCharFormat, QColor, QFont

class LogsTab(QWidget):
    """Processing logs tab with multiple log views"""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.init_ui()
    
    def init_ui(self):
        """Initialize logs tab UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Header
        header_label = QLabel("Processing Logs")
        header_font = QFont()
        header_font.setBold(True)
        header_label.setFont(header_font)
        layout.addWidget(header_label)
        
        # Tab widget for different log types
        self.log_tabs = QTabWidget()
        
        # AI Logs Tab
        self.ai_log_text = QTextEdit()
        self.ai_log_text.setReadOnly(True)
        self.setup_log_text_edit(self.ai_log_text)
        self.log_tabs.addTab(self.ai_log_text, "AI Logs")
        
        # Network Logs Tab
        self.network_log_text = QTextEdit()
        self.network_log_text.setReadOnly(True)
        self.setup_log_text_edit(self.network_log_text)
        self.log_tabs.addTab(self.network_log_text, "Network Logs")
        
        # Program Logs Tab
        self.program_log_text = QTextEdit()
        self.program_log_text.setReadOnly(True)
        self.setup_log_text_edit(self.program_log_text)
        self.log_tabs.addTab(self.program_log_text, "Program Logs")
        
        # All Logs Tab
        self.all_log_text = QTextEdit()
        self.all_log_text.setReadOnly(True)
        self.setup_log_text_edit(self.all_log_text)
        self.log_tabs.addTab(self.all_log_text, "All Logs")
        
        layout.addWidget(self.log_tabs)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.clear_logs_button = QPushButton("Clear All Logs")
        self.clear_logs_button.clicked.connect(self.clear_all_logs)
        
        self.copy_logs_button = QPushButton("Copy Selected Logs")
        self.copy_logs_button.clicked.connect(self.copy_selected_logs)
        
        button_layout.addStretch()
        button_layout.addWidget(self.copy_logs_button)
        button_layout.addWidget(self.clear_logs_button)
        
        layout.addLayout(button_layout)
        
        # Status info
        status_label = QLabel("Logs are updated in real-time during processing")
        status_label.setStyleSheet("color: gray; font-size: 10px;")
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(status_label)
    
    def setup_log_text_edit(self, text_edit):
        """Setup common properties for log text editors"""
        text_edit.setFont(QFont("Consolas", 9))
        text_edit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
    
    def add_ai_log(self, message: str):
        """Add message to AI logs"""
        self.add_colored_log(self.ai_log_text, message, QColor(0, 128, 0))  # Green
        self.add_all_log_entry("AI", message)
    
    def add_network_log(self, message: str):
        """Add message to network logs"""
        self.add_colored_log(self.network_log_text, message, QColor(0, 0, 255))  # Blue
        self.add_all_log_entry("NET", message)
    
    def add_program_log(self, message: str):
        """Add message to program logs"""
        self.add_colored_log(self.program_log_text, message, QColor(128, 0, 128))  # Purple
        self.add_all_log_entry("APP", message)
    
    def add_all_log(self, message: str):
        """Add message to all logs tab"""
        self.all_log_text.append(message)
        self.scroll_to_bottom(self.all_log_text)
    
    def add_colored_log(self, text_edit, message: str, color: QColor):
        """Add colored log message to text edit"""
        cursor = text_edit.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        
        # Create colored format
        format = QTextCharFormat()
        format.setForeground(color)
        
        # Insert message with color
        cursor.insertText(message + "\n", format)
        text_edit.setTextCursor(cursor)
        
        # Scroll to bottom
        self.scroll_to_bottom(text_edit)
    
    def add_all_log_entry(self, category: str, message: str):
        """Add entry to all logs with category prefix"""
        formatted_message = f"[{category}] {message}"
        self.all_log_text.append(formatted_message)
        self.scroll_to_bottom(self.all_log_text)
    
    def scroll_to_bottom(self, text_edit):
        """Scroll text edit to bottom"""
        scrollbar = text_edit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def clear_all_logs(self):
        """Clear all log text areas"""
        self.ai_log_text.clear()
        self.network_log_text.clear()
        self.program_log_text.clear()
        self.all_log_text.clear()
        self.logger.info("All logs cleared")
    
    def copy_selected_logs(self):
        """Copy selected logs to clipboard"""
        current_tab = self.log_tabs.currentWidget()
        if current_tab:
            selected_text = current_tab.textCursor().selectedText()
            if selected_text:
                # In a real implementation, copy to clipboard
                # QApplication.clipboard().setText(selected_text)
                pass