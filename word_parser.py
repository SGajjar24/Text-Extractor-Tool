"""
Parser module for Word documents.
Extracts data from Word documents based on paragraph content defined in the configuration.
"""
import docx
from typing import Dict, List, Any


class WordParser:
    """Parser for extracting data from Word documents."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Word parser with configuration.
        
        Args:
            config: Dictionary containing Word extraction configurations
        """
        self.extraction_rules = config.get('word_extraction', [])
    
    def parse(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Parse a Word document and extract data based on configured extraction rules.
        
        Args:
            file_path: Path to the Word document
            
        Returns:
            List of dictionaries containing extracted data
        """
        results = []
        record = {}
        
        try:
            # Open the Word document
            doc = docx.Document(file_path)
            
            # Process each paragraph
            for paragraph in doc.paragraphs:
                text = paragraph.text.strip()
                if not text:
                    continue
                
                for rule in self.extraction_rules:
                    name = rule.get('name')
                    contains = rule.get('paragraph_contains')
                    extract_after = rule.get('extract_after')
                    value_type = rule.get('type', 'str')
                    
                    if not name or not contains or not extract_after:
                        continue
                    
                    if contains in text:
                        # Extract the text after the specified marker
                        parts = text.split(extract_after, 1)
                        if len(parts) > 1:
                            value = parts[1].strip()
                            
                            # Convert value to specified type
                            if value_type == 'int':
                                try:
                                    value = int(value)
                                except ValueError:
                                    continue
                            elif value_type == 'float':
                                try:
                                    value = float(value)
                                except ValueError:
                                    continue
                            
                            record[name] = value
            
            # If we found any data, add it to results
            if record:
                results.append(record)
                
        except Exception as e:
            print(f"Error parsing Word document {file_path}: {str(e)}")
        
        return results
