"""
Data processor module.
Structures extracted data according to output configuration.
"""
from typing import Dict, List, Any


class DataProcessor:
    """Processor for structuring extracted data according to configuration."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the data processor with configuration.
        
        Args:
            config: Dictionary containing output structure configuration
        """
        self.structure = config.get('structure', [])
    
    def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process and structure the extracted data.
        
        Args:
            data: List of dictionaries containing extracted data
            
        Returns:
            List of dictionaries containing structured data
        """
        if not self.structure or not data:
            return data
        
        structured_data = []
        
        for record in data:
            structured_record = {}
            
            for field_config in self.structure:
                field_name = field_config.get('field')
                if not field_name:
                    continue
                
                # Check if field is required but missing
                required = field_config.get('required', False)
                if required and field_name not in record:
                    print(f"Warning: Required field '{field_name}' is missing in record")
                    continue
                
                # Get value from record
                if field_name in record:
                    value = record[field_name]
                    
                    # Apply formatting if specified
                    format_str = field_config.get('format')
                    if format_str and isinstance(value, (int, float)):
                        try:
                            value = format_str.format(value)
                        except Exception as e:
                            print(f"Error formatting value: {str(e)}")
                    
                    structured_record[field_name] = value
            
            # Only add record if it has data
            if structured_record:
                structured_data.append(structured_record)
        
        return structured_data
