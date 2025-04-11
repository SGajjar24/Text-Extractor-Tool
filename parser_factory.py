"""
Parser factory module.
Creates appropriate parser instances based on file type.
"""
import os
from typing import Dict, List, Any, Optional

from .text_parser import TextParser
from .excel_parser import ExcelParser
from .csv_parser import CSVParser
from .word_parser import WordParser


class ParserFactory:
    """Factory for creating appropriate parser instances based on file type."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the parser factory with configuration.
        
        Args:
            config: Dictionary containing parser configurations
        """
        self.config = config
    
    def get_parser(self, file_path: str) -> Optional[object]:
        """
        Get appropriate parser for the given file.
        
        Args:
            file_path: Path to the file to parse
            
        Returns:
            Parser instance appropriate for the file type, or None if unsupported
        """
        _, ext = os.path.splitext(file_path.lower())
        
        if ext == '.txt':
            return TextParser(self.config)
        elif ext in ['.xlsx', '.xls']:
            return ExcelParser(self.config)
        elif ext == '.csv':
            return CSVParser(self.config)
        elif ext == '.docx':
            return WordParser(self.config)
        else:
            print(f"Unsupported file type: {ext}")
            return None
    
    def parse_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Parse a file using the appropriate parser.
        
        Args:
            file_path: Path to the file to parse
            
        Returns:
            List of dictionaries containing extracted data
        """
        parser = self.get_parser(file_path)
        if parser:
            return parser.parse(file_path)
        return []
