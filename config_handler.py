"""
Configuration handler module.
Loads and validates configuration from YAML files.
"""
import yaml
from typing import Dict, Any, Optional


class ConfigHandler:
    """Handler for loading and validating configuration files."""
    
    def __init__(self):
        """Initialize the configuration handler."""
        self.config = {}
    
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from a YAML file.
        
        Args:
            config_path: Path to the configuration file
            
        Returns:
            Dictionary containing the configuration
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                self.config = yaml.safe_load(file)
                self._validate_config()
                return self.config
        except Exception as e:
            raise ValueError(f"Error loading configuration file: {str(e)}")
    
    def _validate_config(self) -> None:
        """
        Validate the loaded configuration.
        
        Raises:
            ValueError: If the configuration is invalid
        """
        if not self.config:
            raise ValueError("Empty configuration")
        
        # Check for required sections
        if 'input' not in self.config:
            raise ValueError("Missing 'input' section in configuration")
        
        if 'output' not in self.config:
            raise ValueError("Missing 'output' section in configuration")
        
        if 'export' not in self.config:
            raise ValueError("Missing 'export' section in configuration")
        
        # Validate input section
        input_config = self.config['input']
        if not any(key in input_config for key in ['text_patterns', 'excel_mappings', 'word_extraction']):
            raise ValueError("Input section must contain at least one of: 'text_patterns', 'excel_mappings', 'word_extraction'")
        
        # Validate output structure
        output_config = self.config['output']
        if 'structure' not in output_config or not output_config['structure']:
            raise ValueError("Output section must contain a non-empty 'structure' list")
    
    def get_input_config(self) -> Dict[str, Any]:
        """Get the input configuration section."""
        return self.config.get('input', {})
    
    def get_output_config(self) -> Dict[str, Any]:
        """Get the output configuration section."""
        return self.config.get('output', {})
    
    def get_export_config(self) -> Dict[str, Any]:
        """Get the export configuration section."""
        return self.config.get('export', {})
