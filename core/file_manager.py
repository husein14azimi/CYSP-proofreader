"""
File Manager
Handles file operations, naming, and directory management
"""

import logging
from pathlib import Path
from typing import Tuple, List
from config.settings import OUTPUT_FILE_SUFFIX_CLEAN, OUTPUT_FILE_SUFFIX_HIGHLIGHTED

class FileManager:
    """Manages file operations and naming conventions"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_unique_output_filename(self, base_path: str, base_name: str, 
                                 suffix: str, extension: str = ".docx") -> str:
        """
        Generate unique output filename with numbering
        
        Args:
            base_path: Directory path
            base_name: Base filename without extension
            suffix: Suffix to append
            extension: File extension
            
        Returns:
            Unique filename
        """
        base_path_obj = Path(base_path)
        counter = 0
        
        while True:
            if counter == 0:
                filename = f"{base_name}{suffix}{extension}"
            else:
                filename = f"{base_name}{suffix}_{counter}{extension}"
            
            if not (base_path_obj / filename).exists():
                return filename
            counter += 1
    
    def get_output_paths(self, input_path: str, output_dir: str) -> Tuple[str, str]:
        """
        Get paths for both output files
        
        Returns:
            Tuple of (clean_output_path, highlighted_output_path)
        """
        input_path_obj = Path(input_path)
        base_name = input_path_obj.stem
        output_path_obj = Path(output_dir)
        
        clean_filename = self.get_unique_output_filename(
            output_dir, base_name, OUTPUT_FILE_SUFFIX_CLEAN
        )
        highlighted_filename = self.get_unique_output_filename(
            output_dir, base_name, OUTPUT_FILE_SUFFIX_HIGHLIGHTED
        )
        
        clean_path = str(output_path_obj / clean_filename)
        highlighted_path = str(output_path_obj / highlighted_filename)
        
        return clean_path, highlighted_path
    
    def validate_input_file(self, file_path: str) -> Tuple[bool, str]:
        """
        Validate input file exists and is DOCX
        
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        try:
            path = Path(file_path)
            
            if not path.exists():
                return False, "File does not exist"
            
            if not path.is_file():
                return False, "Path is not a file"
            
            if path.suffix.lower() != '.docx':
                return False, "File must be DOCX format"
            
            if path.stat().st_size == 0:
                return False, "File is empty"
            
            return True, "File is valid"
            
        except Exception as e:
            return False, f"File validation error: {str(e)}"
    
    def ensure_output_directory(self, output_dir: str) -> bool:
        """
        Ensure output directory exists
        
        Returns:
            True if directory exists or was created successfully
        """
        try:
            path = Path(output_dir)
            path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            self.logger.error(f"Failed to create output directory: {str(e)}")
            return False
    
    def get_file_info(self, file_path: str) -> dict:
        """
        Get file information for display
        
        Returns:
            Dictionary with file information
        """
        try:
            path = Path(file_path)
            stat = path.stat()
            
            return {
                "name": path.name,
                "size": stat.st_size,
                "modified": stat.st_mtime,
                "extension": path.suffix
            }
        except Exception as e:
            self.logger.error(f"Failed to get file info: {str(e)}")
            return {}

# Convenience function
def create_file_manager() -> FileManager:
    """Factory function to create file manager"""
    return FileManager()