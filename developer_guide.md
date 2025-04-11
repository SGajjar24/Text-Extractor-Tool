"""
Text Extractor Tool - Developer Documentation

This document provides an overview of the Text Extractor tool's architecture and components
for developers who want to understand, modify, or extend the tool.

## Architecture Overview

The Text Extractor tool follows a modular architecture with these main components:

1. **Parsers**: Extract data from different file formats
2. **Configuration Handler**: Load and validate configuration
3. **Data Processor**: Structure the extracted data
4. **Exporters**: Export data to different formats
5. **Main Application**: Orchestrate the process and provide CLI

## Component Details

### Parsers

Located in `src/parser/`, the parsers handle different input formats:

- `text_parser.py`: Extracts data from text files using regex patterns
- `excel_parser.py`: Extracts data from Excel files using column mappings
- `csv_parser.py`: Extracts data from CSV files using column mappings
- `word_parser.py`: Extracts data from Word documents using paragraph content
- `parser_factory.py`: Factory pattern to create appropriate parser based on file extension

### Configuration Handler

Located in `src/config/`, the configuration handler loads and validates YAML configuration:

- `config_handler.py`: Loads, validates, and provides access to configuration sections

### Data Processor

Located in `src/utils/`, the data processor structures the extracted data:

- `data_processor.py`: Structures data according to output configuration

### Exporters

Located in `src/exporters/`, the exporters handle different output formats:

- `excel_exporter.py`: Exports data to Excel format
- `word_exporter.py`: Exports data to Word format
- `text_exporter.py`: Exports data to plain text format

### Main Application

Located in `src/`, the main application orchestrates the process:

- `main.py`: Provides CLI and orchestrates the extraction and export process

## Data Flow

1. User provides input files, configuration file, and output directory
2. Configuration is loaded and validated
3. Input files are processed by appropriate parsers
4. Extracted data is structured by the data processor
5. Structured data is exported to specified formats

## Extending the Tool

### Adding a New Parser

1. Create a new parser class in `src/parser/`
2. Implement the `parse` method that returns a list of dictionaries
3. Update `parser_factory.py` to handle the new file type

### Adding a New Exporter

1. Create a new exporter class in `src/exporters/`
2. Implement the `export` method that takes data and output directory
3. Update `main.py` to handle the new export format

## Testing

The tool includes sample data and a test script:

- `test_extractor.py`: Standalone script for testing the tool
- `sample_data/`: Contains sample files and configuration

## Future Improvements

Potential areas for enhancement:

1. Add support for more input formats (JSON, XML, etc.)
2. Add support for more export formats (PDF, JSON, etc.)
3. Implement more advanced data transformation capabilities
4. Add a graphical user interface
5. Improve error handling and reporting
6. Add unit tests and integration tests
"""
