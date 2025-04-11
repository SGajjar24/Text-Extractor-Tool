"""
Text exporter module.
Exports structured data to plain text format.
"""
import os
from typing import Dict, List, Any


class TextExporter:
    """Exporter for creating text files from structured data."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the text exporter with configuration.
        
        Args:
            config: Dictionary containing text export configurations
        """
        self.config = config.get('text', {})
        self.output_structure = config.get('structure', [])
    
    def export(self, data: List[Dict[str, Any]], output_path: str) -> str:
        """
        Export data to text format.
        
        Args:
            data: List of dictionaries containing structured data
            output_path: Directory path where the output file will be saved
            
        Returns:
            Path to the created text file
        """
        try:
            # Get text-specific settings
            delimiter = self.config.get('delimiter', '|')
            include_header = self.config.get('include_header', True)
            
            # Create mapping of field names to display names
            field_to_display = {
                item.get('field'): item.get('display_name', item.get('field'))
                for item in self.output_structure if 'field' in item
            }
            
            # Get ordered list of fields
            ordered_fields = [item.get('field') for item in self.output_structure if 'field' in item]
            
            # If no structure defined, use all fields from first record
            if not ordered_fields and data:
                ordered_fields = list(data[0].keys())
            
            # Create output file path
            file_name = os.path.join(output_path, 'extracted_data.txt')
            
            with open(file_name, 'w', encoding='utf-8') as file:
                # Write header if requested
                if include_header:
                    header = delimiter.join([field_to_display.get(field, field) for field in ordered_fields])
                    file.write(header + '\n')
                
                # Write data rows
                for record in data:
                    row_values = []
                    for field in ordered_fields:
                        if field in record:
                            # Convert value to string and escape delimiter if present
                            value = str(record[field])
                            if delimiter in value:
                                value = f'"{value}"'
                            row_values.append(value)
                        else:
                            row_values.append('')
                    
                    file.write(delimiter.join(row_values) + '\n')
            
            return file_name
            
        except Exception as e:
            print(f"Error exporting to text: {str(e)}")
            return ""
