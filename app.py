"""
Flask application for the Text Extractor web interface.
Handles file uploads, processes data using the text extraction tool,
and provides download links for the results.
"""
import os
import sys
import uuid
import yaml
import shutil
from flask import Flask, render_template, request, jsonify, send_from_directory, url_for

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import modules from the text extraction tool
from src.config.config_handler import ConfigHandler
from src.parser.parser_factory import ParserFactory
from src.utils.data_processor import DataProcessor
from src.exporters.excel_exporter import ExcelExporter
from src.exporters.word_exporter import WordExporter
from src.exporters.text_exporter import TextExporter

app = Flask(__name__)

# Configure upload and output directories
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), 'outputs')
ALLOWED_INPUT_EXTENSIONS = {'txt', 'xlsx', 'xls', 'csv', 'docx'}
ALLOWED_CONFIG_EXTENSIONS = {'yaml', 'yml'}

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Copy sample config to static folder
SAMPLE_CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'sample_data', 'config_example.yaml')
STATIC_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'static', 'sample_config.yaml')
os.makedirs(os.path.dirname(STATIC_CONFIG_PATH), exist_ok=True)
shutil.copy(SAMPLE_CONFIG_PATH, STATIC_CONFIG_PATH)

@app.route('/')
def index():
    """Render the index page."""
    return render_template('index.html')

@app.route('/sample_config.yaml')
def sample_config():
    """Serve the sample configuration file."""
    return send_from_directory(os.path.join(app.root_path, 'static'), 'sample_config.yaml')

@app.route('/process', methods=['POST'])
def process_files():
    """
    Process uploaded files using the text extraction tool.
    
    Returns:
        JSON response with success status and download links
    """
    try:
        # Create a unique session ID for this request
        session_id = str(uuid.uuid4())
        session_upload_dir = os.path.join(UPLOAD_FOLDER, session_id)
        session_output_dir = os.path.join(OUTPUT_FOLDER, session_id)
        
        # Create session directories
        os.makedirs(session_upload_dir, exist_ok=True)
        os.makedirs(session_output_dir, exist_ok=True)
        
        # Get export formats
        export_formats = request.form.get('exportFormats', 'all')
        
        # Save input files
        input_files = []
        for file in request.files.getlist('inputFiles'):
            if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_INPUT_EXTENSIONS:
                file_path = os.path.join(session_upload_dir, file.filename)
                file.save(file_path)
                input_files.append(file_path)
        
        if not input_files:
            return jsonify({'success': False, 'error': 'No valid input files uploaded'})
        
        # Save config file
        config_file = request.files['configFile']
        if not config_file or '.' not in config_file.filename or \
           config_file.filename.rsplit('.', 1)[1].lower() not in ALLOWED_CONFIG_EXTENSIONS:
            return jsonify({'success': False, 'error': 'Invalid configuration file'})
        
        config_path = os.path.join(session_upload_dir, 'config.yaml')
        config_file.save(config_path)
        
        # Process the files
        result_files = process_extraction(input_files, config_path, session_output_dir, export_formats)
        
        if not result_files:
            return jsonify({'success': False, 'error': 'No data could be extracted from the input files'})
        
        # Generate download URLs
        download_files = []
        for format_name, file_path in result_files.items():
            if file_path:
                file_name = os.path.basename(file_path)
                download_url = url_for('download_file', session_id=session_id, filename=file_name)
                download_files.append({
                    'name': f'Extracted Data ({format_name})',
                    'url': download_url
                })
        
        return jsonify({
            'success': True,
            'files': download_files
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/download/<session_id>/<filename>')
def download_file(session_id, filename):
    """
    Serve a download file from the session output directory.
    
    Args:
        session_id: Unique session ID
        filename: File to download
        
    Returns:
        File for download
    """
    session_output_dir = os.path.join(OUTPUT_FOLDER, session_id)
    return send_from_directory(session_output_dir, filename, as_attachment=True)

def process_extraction(input_files, config_path, output_dir, export_formats):
    """
    Process the extraction using the text extraction tool.
    
    Args:
        input_files: List of input file paths
        config_path: Path to the configuration file
        output_dir: Directory to save output files
        export_formats: Comma-separated list of export formats or "all"
        
    Returns:
        Dictionary mapping format names to output file paths
    """
    try:
        # Load configuration
        config_handler = ConfigHandler()
        config_data = config_handler.load_config(config_path)
        
        # Extract data from input files
        all_data = []
        parser_factory = ParserFactory(config_handler.get_input_config())
        
        for file_path in input_files:
            data = parser_factory.parse_file(file_path)
            if data:
                all_data.extend(data)
        
        if not all_data:
            return {}
        
        # Process and structure the data
        processor = DataProcessor(config_handler.get_output_config())
        structured_data = processor.process(all_data)
        
        # Determine export formats
        if export_formats.lower() == 'all':
            formats = ['excel', 'word', 'text']
        else:
            formats = [fmt.strip().lower() for fmt in export_formats.split(',')]
        
        # Export data to specified formats
        results = {}
        
        # Combine configurations for exporters
        combined_config = {
            **config_handler.get_output_config(),
            **config_handler.get_export_config()
        }
        
        # Export to Excel
        if 'excel' in formats:
            exporter = ExcelExporter(combined_config)
            results['excel'] = exporter.export(structured_data, output_dir)
        
        # Export to Word
        if 'word' in formats:
            exporter = WordExporter(combined_config)
            results['word'] = exporter.export(structured_data, output_dir)
        
        # Export to Text
        if 'text' in formats:
            exporter = TextExporter(combined_config)
            results['text'] = exporter.export(structured_data, output_dir)
        
        return results
        
    except Exception as e:
        print(f"Error in process_extraction: {str(e)}")
        return {}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
