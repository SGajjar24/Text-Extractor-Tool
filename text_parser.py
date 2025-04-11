"""
Parser module for text files.
Extracts data from text files based on regex patterns defined in the configuration.
"""
import re
from typing import Dict, List, Any


class TextParser:
    """Parser for extracting data from text files using regex patterns."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the text parser with configuration.
        
        Args:
            config: Dictionary containing text pattern configurations
        """
        self.patterns = config.get('text_patterns', [])
    
    def parse(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Parse a text file and extract data based on configured patterns.
        
        Args:
            file_path: Path to the text file
            
        Returns:
            List of dictionaries containing extracted data
        """
        results = []
        record = {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
                for pattern_config in self.patterns:
                    name = pattern_config.get('name')
                    pattern = pattern_config.get('pattern')
                    group = pattern_config.get('group', 1)
                    value_type = pattern_config.get('type', 'str')
                    
                    if not name or not pattern:
                        continue
                    
                    matches = re.finditer(pattern, content)
                    for match in matches:
                        try:
                            value = match.group(group)
                            
                            # Convert value to specified type
                            if value_type == 'int':
                                value = int(value)
                            elif value_type == 'float':
                                value = float(value)
                            
                            record[name] = value
                        except (IndexError, ValueError):
                            continue
            
            # If we found any data, add it to results
            if record:
                results.append(record)
                
        except Exception as e:
            print(f"Error parsing text file {file_path}: {str(e)}")
        
        return results
