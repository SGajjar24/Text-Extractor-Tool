"""
Excel exporter module.
Exports structured data to Excel format.
"""
import os
import pandas as pd
from typing import Dict, List, Any


class ExcelExporter:
    """Exporter for creating Excel files from structured data."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Excel exporter with configuration.
        
        Args:
            config: Dictionary containing Excel export configurations
        """
        self.config = config.get('excel', {})
        self.output_structure = config.get('structure', [])
    
    def export(self, data: List[Dict[str, Any]], output_path: str) -> str:
        """
        Export data to Excel format.
        
        Args:
            data: List of dictionaries containing structured data
            output_path: Directory path where the output file will be saved
            
        Returns:
            Path to the created Excel file
        """
        try:
            # Create DataFrame from data
            df = pd.DataFrame(data)
            
            # Reorder and rename columns based on output structure
            if self.output_structure:
                # Create mapping of field names to display names
                field_to_display = {
                    item.get('field'): item.get('display_name', item.get('field'))
                    for item in self.output_structure if 'field' in item
                }
                
                # Get ordered list of fields
                ordered_fields = [item.get('field') for item in self.output_structure if 'field' in item]
                
                # Filter to only include fields that exist in the data
                ordered_fields = [field for field in ordered_fields if field in df.columns]
                
                # Reorder columns
                if ordered_fields:
                    df = df[ordered_fields]
                
                # Rename columns
                df = df.rename(columns=field_to_display)
            
            # Get Excel-specific settings
            sheet_name = self.config.get('sheet_name', 'Extracted Data')
            include_header = self.config.get('include_header', True)
            
            # Create output file path
            file_name = os.path.join(output_path, 'extracted_data.xlsx')
            
            # Export to Excel
            with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
                df.to_excel(
                    writer,
                    sheet_name=sheet_name,
                    index=False,
                    header=include_header
                )
                
                # Apply styling if specified
                if include_header and 'style' in self.config:
                    workbook = writer.book
                    worksheet = writer.sheets[sheet_name]
                    
                    # Apply header styling
                    header_color = self.config.get('style', {}).get('header_color')
                    if header_color:
                        # Note: This is a simplified version. In a real implementation,
                        # we would use openpyxl's styling capabilities more extensively.
                        for col in range(1, len(df.columns) + 1):
                            cell = worksheet.cell(row=1, column=col)
                            # This is a placeholder for actual styling
                            # In a real implementation, we would set the fill color
            
            return file_name
            
        except Exception as e:
            print(f"Error exporting to Excel: {str(e)}")
            return ""
