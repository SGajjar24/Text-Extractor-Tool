# Text Extractor Tool - User Guide

## Overview

Text Extractor is a Python-based tool that extracts data from unorganized files, structures it based on a configuration file, and exports it to multiple formats. The tool supports multiple input formats (text, Excel, CSV, and Word) and can export the structured data to Excel, Word, and plain text formats.

## Features

- **Multiple Input Formats**: Extract data from text files (.txt), Excel files (.xlsx, .xls), CSV files (.csv), and Word documents (.docx)
- **Configurable Extraction**: Define patterns and mappings in a YAML configuration file
- **Data Structuring**: Structure extracted data according to your requirements
- **Multiple Export Formats**: Export to Excel (.xlsx), Word (.docx), and plain text (.txt)
- **Command-Line Interface**: Easy to use from the command line or integrate into scripts

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python test_extractor.py <input_file_or_directory> <config_file> <output_directory> [formats]
```

Where:
- `<input_file_or_directory>`: Path to a single file or directory containing files to process
- `<config_file>`: Path to the YAML configuration file
- `<output_directory>`: Directory where output files will be saved
- `[formats]`: (Optional) Comma-separated list of export formats (excel,word,text) or "all" (default)

### Example

```bash
python test_extractor.py data/orders.txt config.yaml output/ excel,word
```

## Configuration File

The configuration file is in YAML format and has three main sections:

1. `input`: Defines how to extract data from different file types
2. `output`: Defines the structure of the output data
3. `export`: Defines format-specific export settings

### Example Configuration

```yaml
# Input configuration
input:
  # Patterns to extract data from text files
  text_patterns:
    - name: "customer_name"
      pattern: "Customer Name: (.*)"
      group: 1
    - name: "order_id"
      pattern: "Order ID: ([A-Z0-9]+)"
      group: 1
    - name: "total_amount"
      pattern: "Total Amount: \\$(\\d+\\.\\d{2})"
      group: 1
      type: "float"
  
  # Column mappings for Excel/CSV files
  excel_mappings:
    - source_column: "Customer"
      target_field: "customer_name"
    - source_column: "Order Number"
      target_field: "order_id"
    - source_column: "Amount"
      target_field: "total_amount"
      type: "float"
  
  # Word document extraction settings
  word_extraction:
    - name: "customer_name"
      paragraph_contains: "Customer:"
      extract_after: "Customer:"
    - name: "order_id"
      paragraph_contains: "Order ID:"
      extract_after: "Order ID:"
    - name: "total_amount"
      paragraph_contains: "Total:"
      extract_after: "Total:"
      type: "float"

# Output structure configuration
output:
  structure:
    - field: "customer_name"
      display_name: "Customer Name"
      required: true
    - field: "order_id"
      display_name: "Order ID"
      required: true
    - field: "total_amount"
      display_name: "Total Amount"
      format: "${:.2f}"
      required: true

# Export configuration
export:
  excel:
    sheet_name: "Extracted Data"
    include_header: true
    style:
      header_color: "#CCCCCC"
  
  word:
    title: "Extracted Data Report"
    include_table: true
    include_summary: true
  
  text:
    delimiter: "|"
    include_header: true
```

## Input Configuration Details

### Text Patterns

For text files, define regex patterns to extract data:

- `name`: Field name for the extracted data
- `pattern`: Regular expression pattern with capture groups
- `group`: Which capture group to use (default: 1)
- `type`: Data type conversion (str, int, float)

### Excel/CSV Mappings

For Excel and CSV files, define column mappings:

- `source_column`: Column name in the source file
- `target_field`: Field name for the extracted data
- `type`: Data type conversion (str, int, float)

### Word Extraction

For Word documents, define paragraph-based extraction:

- `name`: Field name for the extracted data
- `paragraph_contains`: Text to identify the paragraph
- `extract_after`: Text after which to extract the value
- `type`: Data type conversion (str, int, float)

## Output Structure

Define the structure of the output data:

- `field`: Field name from the extracted data
- `display_name`: Display name for the field in outputs
- `required`: Whether the field is required
- `format`: Format string for the field value

## Export Configuration

### Excel Export

- `sheet_name`: Name of the worksheet
- `include_header`: Whether to include headers
- `style`: Styling options for the Excel file

### Word Export

- `title`: Title for the Word document
- `include_table`: Whether to include a data table
- `include_summary`: Whether to include a summary

### Text Export

- `delimiter`: Character to use as field delimiter
- `include_header`: Whether to include headers

## Extending the Tool

The tool is designed to be modular and extensible. You can:

1. Add support for new input formats by creating new parser classes
2. Add support for new export formats by creating new exporter classes
3. Enhance the data processing logic in the DataProcessor class

## Troubleshooting

- If no data is extracted, check that your configuration patterns match the input files
- If required fields are missing, you'll see warnings in the output
- For import errors, use the standalone test_extractor.py script

## License

MIT
