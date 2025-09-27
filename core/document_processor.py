"""
Document Processor
Handles DOCX reading, processing, and output generation
"""

import logging
from pathlib import Path
from typing import Tuple, List
import docx
from docx.document import Document as DocxDocument
import mammoth
import markdown
from utils.converters import markdown_to_docx
from core.ai_handler import AIHandler
from utils.logger import get_processing_logger

class DocumentProcessor:
    """Main document processing class"""
    
    def __init__(self):
        self.logger = get_processing_logger()
        self.ai_handler = None
        self.current_model = None
        
    def set_ai_handler(self, ai_handler: AIHandler):
        """Set AI handler for processing"""
        self.ai_handler = ai_handler
        
    def set_model(self, model_name: str):
        """Set current model for processing"""
        self.current_model = model_name
        self.logger.info(f"Model set to: {model_name}")
        
    def process_document(self, input_path: str, output_dir: str) -> Tuple[bool, str]:
        """
        Process entire document through AI
        
        Args:
            input_path: Path to input DOCX file
            output_dir: Directory for output files
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            self.logger.info(f"Starting document processing: {input_path}")
            
            # Check if model is set
            if not self.current_model:
                return False, "No AI model selected. Please configure a model in API tab."
            
            # Convert DOCX to Markdown
            markdown_content, token_count = self._docx_to_markdown(input_path)
            self.logger.info(f"Document converted to Markdown. Tokens: {token_count}")
            
            # Validate token limit
            max_tokens = self.ai_handler.get_model_max_tokens(self.current_model)
            if token_count > max_tokens:
                return False, f"Document too large ({token_count} tokens). Max: {max_tokens}"
            
            # Process with AI
            self.logger.info(f"Sending to AI model: {self.current_model}")
            edited_markdown = self.ai_handler.process_text(markdown_content, self.current_model)
            
            if not edited_markdown:
                return False, "AI processing failed - empty response"
            
            # Generate single output file
            success, message = self._generate_output_file(
                input_path, output_dir, edited_markdown
            )
            
            if success:
                self.logger.info("Document processing completed successfully")
            else:
                self.logger.error(f"Output generation failed: {message}")
                
            return success, message
            
        except Exception as e:
            self.logger.error(f"Document processing failed: {str(e)}")
            return False, f"Processing error: {str(e)}"
    
    def _docx_to_markdown(self, docx_path: str) -> Tuple[str, int]:
        """
        Convert DOCX to Markdown and count tokens
        
        Returns:
            Tuple of (markdown_content: str, token_count: int)
        """
        try:
            # Convert DOCX to Markdown
            with open(docx_path, "rb") as docx_file:
                result = mammoth.convert_to_markdown(docx_file)
                markdown_content = result.value
            
            # Count tokens
            token_count = self.ai_handler.count_tokens(markdown_content, self.current_model)
            
            return markdown_content, token_count
            
        except Exception as e:
            self.logger.error(f"DOCX to Markdown conversion failed: {str(e)}")
            raise
    
    def _generate_output_file(self, input_path: str, output_dir: str, 
                            edited_md: str) -> Tuple[bool, str]:
        """
        Generate single output file with AI-edited content
        """
        try:
            input_path_obj = Path(input_path)
            base_name = input_path_obj.stem
            output_path_obj = Path(output_dir)
            
            # Generate single output file
            output_filename = self._get_unique_filename(
                output_path_obj, base_name, "_Edited"
            )
            output_path = output_path_obj / output_filename
            
            success = self._save_docx(edited_md, str(output_path))
            if not success:
                return False, "Failed to generate output file"
            
            return True, f"File generated: {output_filename}"
            
        except Exception as e:
            self.logger.error(f"Output file generation failed: {str(e)}")
            return False, f"Output generation error: {str(e)}"
    
    def _save_docx(self, markdown_content: str, output_path: str) -> bool:
        """Save DOCX file from Markdown"""
        try:
            doc = markdown_to_docx(markdown_content)
            doc.save(output_path)
            self.logger.info(f"DOCX saved: {output_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save DOCX: {str(e)}")
            return False
    
    def _get_unique_filename(self, directory: Path, base_name: str, suffix: str) -> str:
        """Generate unique filename with numbering"""
        counter = 0
        while True:
            if counter == 0:
                filename = f"{base_name}{suffix}.docx"
            else:
                filename = f"{base_name}{suffix}_{counter}.docx"
            
            if not (directory / filename).exists():
                return filename
            counter += 1

# Convenience function
def create_document_processor() -> DocumentProcessor:
    """Factory function to create document processor"""
    return DocumentProcessor()