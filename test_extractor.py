"""
Standalone test script for the Text Extractor tool.
This script avoids import issues by importing modules directly.
"""
import os
import sys
import click
from typing import Dict, List, Any

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import modules directly
from src.config.config_handler import ConfigHandler
from src.parser.parser_factory import ParserFactory
from src.utils.data_processor import DataProcessor
from src.exporters.excel_exporter import ExcelExporter
from src.exporters.word_exporter import WordExporter
from src.exporters.text_exporter import TextExporter


def main(input_path, config_path, output_path, formats='all'):
    """
    Extract data from files and export to specified formats.
    
    Args:
        input_path: Input file or directory path
        config_path: Configuration file path
        output_path: Output directory path
        formats: Output formats (comma-separated: excel,word,text or "all")
    """
    try:
        # Load configuration
        config_handler = ConfigHandler()
        config_data = config_handler.load_config(config_path)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        
        # Process input files
        input_files = get_input_files(input_path)
        if not input_files:
            print(f"No supported files found in {input_path}")
            return
        
        # Extract data from input files
        extracted_data = extract_data(input_files, config_handler.get_input_config())
        if not extracted_data:
            print("No data extracted from input files")
            return
        
        # Process and structure the data
        processor = DataProcessor(config_handler.get_output_config())
        structured_data = processor.process(extracted_data)
        
        # Determine export formats
        export_formats = determine_export_formats(formats)
        
        # Export data to specified formats
        export_results = export_data(
            structured_data, 
            output_path, 
            export_formats, 
            config_handler.get_output_config(),
            config_handler.get_export_config()
        )
        
        # Print results
        print(f"Processed {len(input_files)} files and extracted {len(structured_data)} records")
        for format_name, file_path in export_results.items():
            if file_path:
                print(f"Exported to {format_name}: {file_path}")
        
        return export_results
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {}


def get_input_files(input_path: str) -> List[str]:
    """
    Get list of supported input files from the input path.
    
    Args:
        input_path: Input file or directory path
        
    Returns:
        List of file paths
    """
    supported_extensions = ['.txt', '.xlsx', '.xls', '.csv', '.docx']
    
    if os.path.isfile(input_path):
        _, ext = os.path.splitext(input_path.lower())
        if ext in supported_extensions:
            return [input_path]
        else:
            return []
    
    elif os.path.isdir(input_path):
        files = []
        for root, _, filenames in os.walk(input_path):
            for filename in filenames:
                _, ext = os.path.splitext(filename.lower())
                if ext in supported_extensions:
                    files.append(os.path.join(root, filename))
        return files
    
    return []


def extract_data(input_files: List[str], config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract data from input files.
    
    Args:
        input_files: List of input file paths
        config: Input configuration
        
    Returns:
        List of dictionaries containing extracted data
    """
    all_data = []
    parser_factory = ParserFactory(config)
    
    for file_path in input_files:
        data = parser_factory.parse_file(file_path)
        if data:
            all_data.extend(data)
    
    return all_data


def determine_export_formats(formats_str: str) -> List[str]:
    """
    Determine which export formats to use.
    
    Args:
        formats_str: Comma-separated list of formats or "all"
        
    Returns:
        List of format names
    """
    if formats_str.lower() == 'all':
        return ['excel', 'word', 'text']
    
    return [fmt.strip().lower() for fmt in formats_str.split(',')]


def export_data(
    data: List[Dict[str, Any]], 
    output_dir: str, 
    formats: List[str],
    output_config: Dict[str, Any],
    export_config: Dict[str, Any]
) -> Dict[str, str]:
    """
    Export data to specified formats.
    
    Args:
        data: List of dictionaries containing structured data
        output_dir: Output directory path
        formats: List of export formats
        output_config: Output configuration
        export_config: Export configuration
        
    Returns:
        Dictionary mapping format names to output file paths
    """
    results = {}
    
    # Combine configurations for exporters
    combined_config = {
        **output_config,
        **export_config
    }
    
    # Export to Excel
    if 'excel' in formats:
        exporter = ExcelExporter(combined_config)
        results['excel'] = exporter.export(data, output_dir)
    
    # Export to Word
    if 'word' in formats:
        exporter = WordExporter(combined_config)
        results['word'] = exporter.export(data, output_dir)
    
    # Export to Text
    if 'text' in formats:
        exporter = TextExporter(combined_config)
        results['text'] = exporter.export(data, output_dir)
    
    return results


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python test_extractor.py <input_path> <config_path> <output_path> [formats]")
        sys.exit(1)
    
    input_path = sys.argv[1]
    config_path = sys.argv[2]
    output_path = sys.argv[3]
    formats = sys.argv[4] if len(sys.argv) > 4 else 'all'
    
    main(input_path, config_path, output_path, formats)
