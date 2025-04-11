"""
Parser module for Excel files.
Extracts data from Excel files based on column mappings defined in the configuration.
"""
import pandas as pd
from typing import Dict, List, Any


class ExcelParser:
    """Parser for extracting data from Excel files using column mappings."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Excel parser with configuration.
        
        Args:
            config: Dictionary containing Excel mapping configurations
        """
        self.mappings = config.get('excel_mappings', [])
    
    def parse(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Parse an Excel file and extract data based on configured column mappings.
        
        Args:
            file_path: Path to the Excel file
            
        Returns:
            List of dictionaries containing extracted data
        """
        results = []
        
        try:
            # Read Excel file
            df = pd.read_excel(file_path)
            
            # Process each row
            for _, row in df.iterrows():
                record = {}
                
                for mapping in self.mappings:
                    source_column = mapping.get('source_column')
                    target_field = mapping.get('target_field')
                    value_type = mapping.get('type', 'str')
                    
                    if not source_column or not target_field or source_column not in row:
                        continue
                    
                    value = row[source_column]
                    
                    # Convert value to specified type
                    if value_type == 'int' and pd.notna(value):
                        value = int(value)
                    elif value_type == 'float' and pd.notna(value):
                        value = float(value)
                    
                    record[target_field] = value
                
                # If we found any data, add it to results
                if record:
                    results.append(record)
                
        except Exception as e:
            print(f"Error parsing Excel file {file_path}: {str(e)}")
        
        return results
