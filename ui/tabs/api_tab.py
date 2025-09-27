"""
API Configuration Tab
Handles API key input and model selection
"""

import logging
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                            QLineEdit, QPushButton, QComboBox, QLabel, 
                            QGroupBox, QMessageBox, QStackedWidget, QSpinBox)
from PyQt6.QtCore import Qt, pyqtSignal
from config.models import get_available_models, DEFAULT_MODEL, is_model_available

class APITab(QWidget):
    """API configuration tab"""
    
    # Signals
    api_key_changed = pyqtSignal(str)
    model_changed = pyqtSignal(str)
    
    def __init__(self, ai_handler):
        super().__init__()
        self.ai_handler = ai_handler
        self.logger = logging.getLogger(__name__)
        self.init_ui()
    
    def init_ui(self):
        """Initialize API tab UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # API Key Group
        api_group = QGroupBox("OpenRouter API Configuration")
        api_layout = QVBoxLayout(api_group)
        
        # API key input - now auto-applies
        key_layout = QHBoxLayout()
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setPlaceholderText("Enter your OpenRouter API key")
        self.api_key_input.textChanged.connect(self.on_api_key_changed)  # Auto-apply
        
        self.show_key_button = QPushButton("👁")
        self.show_key_button.setFixedWidth(30)
        self.show_key_button.setCheckable(True)
        self.show_key_button.clicked.connect(self.toggle_key_visibility)
        
        key_layout.addWidget(QLabel("API Key:"))
        key_layout.addWidget(self.api_key_input)
        key_layout.addWidget(self.show_key_button)
        
        api_layout.addLayout(key_layout)
        
        # API key info
        info_label = QLabel(
            "Get your free API key from: https://openrouter.ai/keys\n"
            "Your key is stored only in memory and never saved to disk."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: gray; font-size: 10px;")
        api_layout.addWidget(info_label)
        
        layout.addWidget(api_group)
        
        # Model Selection Group
        model_group = QGroupBox("AI Model Selection")
        model_layout = QVBoxLayout(model_group)
        
        # Model selection method
        method_layout = QHBoxLayout()
        self.method_combo = QComboBox()
        self.method_combo.addItem("Recommended Models", "recommended")
        self.method_combo.addItem("Custom Model Name", "custom")
        self.method_combo.currentIndexChanged.connect(self.on_method_changed)
        
        method_layout.addWidget(QLabel("Selection Method:"))
        method_layout.addWidget(self.method_combo)
        method_layout.addStretch()
        
        model_layout.addLayout(method_layout)
        
        # Stacked widget for different selection methods
        self.model_stack = QStackedWidget()
        
        # Recommended models page
        recommended_page = QWidget()
        recommended_layout = QVBoxLayout(recommended_page)
        
        self.recommended_combo = QComboBox()
        self.populate_recommended_models()
        recommended_layout.addWidget(QLabel("Select Recommended Model:"))
        recommended_layout.addWidget(self.recommended_combo)
        
        # Custom model page
        custom_page = QWidget()
        custom_layout = QVBoxLayout(custom_page)
        
        # Custom model name
        self.custom_model_input = QLineEdit()
        self.custom_model_input.setPlaceholderText("Enter full model name (e.g., deepseek/deepseek-chat-v3.1:free)")
        custom_layout.addWidget(QLabel("Enter Custom Model Name:"))
        custom_layout.addWidget(self.custom_model_input)
        
        # Custom token limit
        self.token_limit_input = QSpinBox()
        self.token_limit_input.setRange(1000, 1000000)  # 1K to 1M tokens
        self.token_limit_input.setValue(128000)  # Default
        self.token_limit_input.setSuffix(" tokens")
        
        custom_layout.addWidget(QLabel("Token Limit (for validation):"))
        custom_layout.addWidget(self.token_limit_input)
        
        self.model_stack.addWidget(recommended_page)
        self.model_stack.addWidget(custom_page)
        self.model_stack.setCurrentIndex(0)
        
        model_layout.addWidget(self.model_stack)
        
        # Model info
        self.model_info_label = QLabel()
        self.model_info_label.setWordWrap(True)
        self.model_info_label.setStyleSheet("color: gray;")
        model_layout.addWidget(self.model_info_label)
        
        layout.addWidget(model_group)
        
        # Current status
        self.status_label = QLabel("API not configured")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Spacer
        layout.addStretch()
        
        # Set initial model
        self.update_model_info()
    
    def populate_recommended_models(self):
        """Populate recommended model selection combo box"""
        self.recommended_combo.clear()
        models = get_available_models()
        
        for model_name, display_name in models:
            self.recommended_combo.addItem(display_name, model_name)
        
        # Set default model
        default_index = self.recommended_combo.findData(DEFAULT_MODEL)
        if default_index >= 0:
            self.recommended_combo.setCurrentIndex(default_index)
        
        self.recommended_combo.currentIndexChanged.connect(self.on_recommended_model_changed)
    
    def on_method_changed(self):
        """Handle selection method change"""
        current_index = self.method_combo.currentData()
        if current_index == "recommended":
            self.model_stack.setCurrentIndex(0)
            self.on_recommended_model_changed()
        else:
            self.model_stack.setCurrentIndex(1)
            self.on_custom_model_changed()
    
    def on_recommended_model_changed(self):
        """Handle recommended model selection change"""
        model_name = self.recommended_combo.currentData()
        if model_name:
            self.model_changed.emit(model_name)
            self.update_model_info()
    
    def on_custom_model_changed(self):
        """Handle custom model name change"""
        model_name = self.custom_model_input.text().strip()
        if model_name:
            self.model_changed.emit(model_name)
            self.update_model_info()
    
    def toggle_key_visibility(self):
        """Toggle API key visibility"""
        if self.show_key_button.isChecked():
            self.api_key_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_key_button.setText("🔒")
        else:
            self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_key_button.setText("👁")
    
    def on_api_key_changed(self):
        """Auto-apply API key when text changes"""
        api_key = self.api_key_input.text().strip()
        
        if api_key:
            try:
                # Set API key in AI handler
                self.ai_handler.set_api_key(api_key)
                
                # Emit signal
                self.api_key_changed.emit(api_key)
                
                # Update status
                self.status_label.setText("API key configured")
                self.status_label.setStyleSheet("color: green;")
                
                self.logger.info("API key configured automatically")
                
            except Exception as e:
                error_msg = f"Failed to configure API key: {str(e)}"
                self.logger.error(error_msg)
                self.status_label.setText("API configuration failed")
                self.status_label.setStyleSheet("color: red;")
        else:
            # Clear API key if empty
            self.ai_handler.api_key = None
            self.status_label.setText("API not configured")
            self.status_label.setStyleSheet("")
    
    def update_model_info(self):
        """Update model information display"""
        if self.method_combo.currentData() == "recommended":
            model_name = self.recommended_combo.currentData()
            is_recommended = is_model_available(model_name)
            if is_recommended:
                self.model_info_label.setText(f"Recommended model: {model_name}")
            else:
                self.model_info_label.setText(f"Model: {model_name}")
        else:
            model_name = self.custom_model_input.text().strip()
            token_limit = self.token_limit_input.value()
            if model_name:
                self.model_info_label.setText(f"Custom model: {model_name} | Token limit: {token_limit}")