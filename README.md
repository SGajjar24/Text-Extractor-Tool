# Text Extractor Tool

A Python-based tool that extracts data from unorganized files, structures it based on a configuration file, and exports it to multiple formats.

## Features

- Extract data from multiple file formats:
  - Text files (.txt)
  - Excel files (.xlsx, .xls)
  - CSV files (.csv)
  - Word documents (.docx)
- Structure data according to user-defined configuration
- Export data to multiple formats:
  - Excel (.xlsx)
  - Word (.docx)
  - Plain text (.txt)

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m text_extractor.main --input <input_file_or_directory> --config <config_file> --output <output_directory>
```

### Configuration File

The configuration file (YAML format) defines how to extract and structure data from the input files. See `sample_data/config_example.yaml` for an example.

## License

MIT
