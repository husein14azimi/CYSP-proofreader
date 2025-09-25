"""
Document Format Converters
Handles conversion between DOCX, Markdown, and other formats
"""

import logging
from typing import Tuple, Optional
import docx
from docx.document import Document as DocxDocument
from docx.shared import RGBColor
import mammoth
import markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

class Converters:
    """Collection of document conversion utilities"""
    
    @staticmethod
    def docx_to_markdown(docx_path: str) -> Tuple[str, dict]:
        """
        Convert DOCX to Markdown
        
        Args:
            docx_path: Path to DOCX file
            
        Returns:
            Tuple of (markdown_content: str, conversion_info: dict)
        """
        try:
            with open(docx_path, "rb") as docx_file:
                result = mammoth.convert_to_markdown(docx_file)
                
                conversion_info = {
                    "messages": result.messages,
                    "warnings": len([m for m in result.messages if m.type == "warning"]),
                    "errors": len([m for m in result.messages if m.type == "error"])
                }
                
                return result.value, conversion_info
                
        except Exception as e:
            logging.error(f"DOCX to Markdown conversion failed: {str(e)}")
            raise

    @staticmethod
    def markdown_to_docx(markdown_content: str) -> DocxDocument:
        """
        Convert Markdown to DOCX document
        
        Args:
            markdown_content: Markdown text to convert
            
        Returns:
            DOCX Document object
        """
        try:
            # Create new document
            doc = docx.Document()
            
            # Parse markdown and convert to DOCX
            # This is a simplified implementation
            lines = markdown_content.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    doc.add_paragraph()
                elif line.startswith('# '):
                    # Heading 1
                    doc.add_heading(line[2:], level=1)
                elif line.startswith('## '):
                    # Heading 2
                    doc.add_heading(line[3:], level=2)
                elif line.startswith('### '):
                    # Heading 3
                    doc.add_heading(line[4:], level=3)
                elif line.startswith('- ') or line.startswith('* '):
                    # Bullet point
                    doc.add_paragraph(line[2:], style='List Bullet')
                elif line.startswith('1. '):
                    # Numbered list
                    doc.add_paragraph(line[3:], style='List Number')
                else:
                    # Regular paragraph
                    doc.add_paragraph(line)
            
            return doc
            
        except Exception as e:
            logging.error(f"Markdown to DOCX conversion failed: {str(e)}")
            raise

    @staticmethod
    def apply_highlighting_to_docx(original_doc: DocxDocument, 
                                 edited_doc: DocxDocument) -> DocxDocument:
        """
        Apply highlighting to show changes between documents
        
        Args:
            original_doc: Original DOCX document
            edited_doc: Edited DOCX document
            
        Returns:
            DOCX document with highlighted changes
        """
        try:
            # Create result document
            result_doc = docx.Document()
            
            # This is a simplified implementation
            # In practice, you'd want to do proper diff comparison
            for i, (orig_para, edit_para) in enumerate(zip(original_doc.paragraphs, edited_doc.paragraphs)):
                # Add paragraph with basic formatting
                new_para = result_doc.add_paragraph()
                
                # Copy text with basic formatting
                for run in edit_para.runs:
                    new_run = new_para.add_run(run.text)
                    new_run.font.name = run.font.name
                    new_run.font.size = run.font.size
                    
                    # Apply highlighting for demonstration
                    # In real implementation, compare with original
                    if i % 3 == 0:  # Just for demo - highlight some paragraphs
                        new_run.font.highlight_color = docx.enum.text.WD_COLOR.YELLOW
            
            return result_doc
            
        except Exception as e:
            logging.error(f"Highlighting application failed: {str(e)}")
            raise

def markdown_to_docx(markdown_content: str) -> DocxDocument:
    """Convenience function for markdown to DOCX conversion"""
    return Converters.markdown_to_docx(markdown_content)

def docx_to_markdown(docx_path: str) -> Tuple[str, dict]:
    """Convenience function for DOCX to markdown conversion"""
    return Converters.docx_to_markdown(docx_path)

def apply_highlighting(original_doc: DocxDocument, edited_doc: DocxDocument) -> DocxDocument:
    """Convenience function for applying highlighting"""
    return Converters.apply_highlighting_to_docx(original_doc, edited_doc)