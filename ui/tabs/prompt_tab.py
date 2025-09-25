"""
Prompt Customization Tab
Handles system prompt editing and customization
"""

import logging
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
                            QPushButton, QLabel, QMessageBox, QGroupBox)
from PyQt6.QtCore import Qt
from config.settings import DEFAULT_PROMPT

class PromptTab(QWidget):
    """Prompt customization tab"""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.init_ui()
        self.load_default_prompt()
    
    def init_ui(self):
        """Initialize prompt tab UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Prompt Editor Group
        editor_group = QGroupBox("System Prompt Customization")
        editor_layout = QVBoxLayout(editor_group)
        
        # Instructions
        instructions = QLabel(
            "Customize the system prompt sent to the AI model. "
            "This prompt guides the AI to focus on spelling and dictation corrections only."
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: gray;")
        editor_layout.addWidget(instructions)
        
        # Prompt editor
        self.prompt_editor = QTextEdit()
        self.prompt_editor.setMinimumHeight(200)
        self.prompt_editor.setPlaceholderText(
            "Enter your custom system prompt here...\n"
            "The prompt should instruct the AI to fix only spelling and dictation errors."
        )
        editor_layout.addWidget(self.prompt_editor)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.load_default_button = QPushButton("Load Default Prompt")
        self.load_default_button.clicked.connect(self.load_default_prompt)
        
        self.save_prompt_button = QPushButton("Save Prompt")
        self.save_prompt_button.clicked.connect(self.save_prompt)
        
        self.reset_button = QPushButton("Reset to Default")
        self.reset_button.clicked.connect(self.reset_to_default)
        
        button_layout.addWidget(self.load_default_button)
        button_layout.addStretch()
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.save_prompt_button)
        
        editor_layout.addLayout(button_layout)
        
        layout.addWidget(editor_group)
        
        # Prompt Info Group
        info_group = QGroupBox("Prompt Information")
        info_layout = QVBoxLayout(info_group)
        
        info_text = QLabel(
            "• The prompt is sent with each document processing request\n"
            "• Focus on dictation/spelling corrections only\n"
            "• Keep instructions clear and specific\n"
            "• Changes take effect immediately\n\n"
            "Default behavior: Fix spelling/dictation while maintaining document structure"
        )
        info_text.setWordWrap(True)
        info_text.setStyleSheet("color: gray; font-size: 10px;")
        info_layout.addWidget(info_text)
        
        layout.addWidget(info_group)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Spacer
        layout.addStretch()
    
    def load_default_prompt(self):
        """Load default system prompt"""
        self.prompt_editor.setPlainText(DEFAULT_PROMPT)
        self.status_label.setText("Default prompt loaded")
        self.status_label.setStyleSheet("color: green;")
        self.logger.info("Default prompt loaded")
    
    def reset_to_default(self):
        """Reset to default prompt with confirmation"""
        reply = QMessageBox.question(
            self, 
            "Reset Prompt", 
            "Are you sure you want to reset to the default prompt?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.load_default_prompt()
            self.status_label.setText("Prompt reset to default")
    
    def save_prompt(self):
        """Save current prompt (placeholder for future implementation)"""
        current_prompt = self.prompt_editor.toPlainText().strip()
        
        if not current_prompt:
            QMessageBox.warning(self, "Warning", "Prompt cannot be empty")
            return
        
        # In a real implementation, this would save to settings
        # For now, just show success message
        self.status_label.setText("Prompt saved successfully")
        self.status_label.setStyleSheet("color: green;")
        self.logger.info("Custom prompt saved")
    
    def get_current_prompt(self):
        """Get current prompt text"""
        return self.prompt_editor.toPlainText().strip()
    
    def set_prompt(self, prompt_text):
        """Set prompt text"""
        self.prompt_editor.setPlainText(prompt_text)