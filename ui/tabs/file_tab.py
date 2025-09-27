"""
File Selection Tab
Handles file selection, processing initiation, and progress display
"""

import logging
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                            QFileDialog, QLabel, QProgressBar, QTextEdit,
                            QGroupBox, QGridLayout)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QObject
from pathlib import Path

class ProcessingWorker(QObject):
    """Worker class for processing documents in separate thread"""
    finished = pyqtSignal(bool, str)  # success, message
    started = pyqtSignal()
    
    def __init__(self, document_processor, file_path, output_dir):
        super().__init__()
        self.document_processor = document_processor
        self.file_path = file_path
        self.output_dir = output_dir
    
    def process(self):
        """Process document in separate thread"""
        self.started.emit()
        try:
            success, message = self.document_processor.process_document(
                self.file_path, self.output_dir
            )
            self.finished.emit(success, message)
        except Exception as e:
            self.finished.emit(False, f"Processing error: {str(e)}")

class FileTab(QWidget):
    """File selection and processing tab"""
    
    # Signals
    process_started = pyqtSignal()
    process_completed = pyqtSignal(str)
    process_error = pyqtSignal(str)
    
    def __init__(self, file_manager, document_processor):
        super().__init__()
        self.file_manager = file_manager
        self.document_processor = document_processor
        self.selected_file = None
        self.logger = logging.getLogger(__name__)
        self.processing_thread = None
        self.worker = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize file tab UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # File Selection Group
        file_group = QGroupBox("Document Selection")
        file_layout = QVBoxLayout(file_group)
        
        # File selection controls
        file_select_layout = QHBoxLayout()
        self.file_path_label = QLabel("No file selected")
        self.file_path_label.setWordWrap(True)
        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self.browse_file)
        file_select_layout.addWidget(self.file_path_label)
        file_select_layout.addWidget(self.browse_button)
        
        file_layout.addLayout(file_select_layout)
        
        # File info display
        self.file_info_label = QLabel("")
        self.file_info_label.setStyleSheet("color: gray;")
        file_layout.addWidget(self.file_info_label)
        
        layout.addWidget(file_group)
        
        # Processing Controls Group
        process_group = QGroupBox("Processing")
        process_layout = QVBoxLayout(process_group)
        
        # Process button
        self.process_button = QPushButton("Process Document")
        self.process_button.clicked.connect(self.process_document)
        self.process_button.setEnabled(False)
        process_layout.addWidget(self.process_button)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        process_layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        process_layout.addWidget(self.status_label)
        
        layout.addWidget(process_group)
        
        # Spacer
        layout.addStretch()
    
    def browse_file(self):
        """Open file dialog to select DOCX file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Document", 
            "", 
            "Word Documents (*.docx)"
        )
        
        if file_path:
            self.select_file(file_path)
    
    def select_file(self, file_path: str):
        """Select and validate file"""
        # Validate file
        is_valid, message = self.file_manager.validate_input_file(file_path)
        
        if is_valid:
            self.selected_file = file_path
            self.file_path_label.setText(f"Selected: {Path(file_path).name}")
            self.process_button.setEnabled(True)
            
            # Show file info
            file_info = self.file_manager.get_file_info(file_path)
            if file_info:
                size_kb = file_info['size'] / 1024
                self.file_info_label.setText(f"Size: {size_kb:.1f} KB")
            
            self.logger.info(f"File selected: {file_path}")
            self.status_label.setText("File ready for processing")
        else:
            self.selected_file = None
            self.file_path_label.setText("No file selected")
            self.process_button.setEnabled(False)
            self.file_info_label.setText("")
            self.status_label.setText(f"Error: {message}")
            self.logger.warning(f"File validation failed: {message}")
    
    def process_document(self):
        """Start document processing in separate thread"""
        if not self.selected_file:
            self.status_label.setText("Please select a file first")
            return
        
        # Emit signal that processing is starting
        self.process_started.emit()
        
        # Setup UI for processing
        self.process_button.setEnabled(False)
        self.browse_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.status_label.setText("Processing document...")
        
        # Create thread and worker
        self.processing_thread = QThread()
        self.worker = ProcessingWorker(
            self.document_processor, 
            self.selected_file, 
            str(Path(self.selected_file).parent)
        )
        
        # Move worker to thread
        self.worker.moveToThread(self.processing_thread)
        
        # Connect signals
        self.worker.started.connect(lambda: self.logger.info("Processing started in thread"))
        self.worker.finished.connect(self.on_processing_finished)
        self.processing_thread.started.connect(self.worker.process)
        
        # Start the thread
        self.processing_thread.start()
    
    def on_processing_finished(self, success, message):
        """Handle processing completion from thread"""
        # Clean up thread
        if self.processing_thread:
            self.processing_thread.quit()
            self.processing_thread.wait()
            self.processing_thread = None
            self.worker = None
        
        # Update UI based on result
        if success:
            self.process_completed.emit(message)
            self.status_label.setText("Processing completed successfully!")
            self.logger.info(f"Processing completed: {message}")
        else:
            self.process_error.emit(message)
            self.status_label.setText(f"Error: {message}")
            self.logger.error(f"Processing failed: {message}")
        
        # Reset UI
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 100)
        self.process_button.setEnabled(True)
        self.browse_button.setEnabled(True)