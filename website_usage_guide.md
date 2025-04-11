# Text Extractor Tool - Website Usage Guide

## Overview

The Text Extractor Tool is now available as a website, allowing you to access its functionality through a web browser without needing to install anything locally. This guide explains how to use the website version of the tool.

## Accessing the Website

The Text Extractor Tool website is permanently deployed at:

**[https://jhughalo.manus.space](https://jhughalo.manus.space)**

You can access this website from any device with a web browser.

## Website Features

The website provides information about the Text Extractor Tool, including:

1. **Tool Overview**: A description of what the tool does and its key features
2. **Feature List**: Details about supported input formats, configuration options, and export formats
3. **Usage Instructions**: Step-by-step guide on how to use the tool
4. **Configuration Examples**: Sample YAML configuration file with explanations
5. **Command Line Examples**: Examples of how to use the command-line version

## Using the Tool

While the website primarily serves as documentation for the Text Extractor Tool, you can download all necessary files to use the tool locally:

1. **Download the Tool**: Click the "Download from GitHub" button to get the complete tool
2. **Download Sample Configuration**: Click the "Download Sample Configuration" button to get a sample YAML configuration file

## Local Installation

After downloading the tool, follow these steps to install it locally:

1. Extract the downloaded files to a directory on your computer
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create or modify the configuration file to match your data extraction needs
4. Run the tool using the command line:
   ```bash
   python test_extractor.py <input_file_or_directory> <config_file> <output_directory>
   ```

## Configuration File

The configuration file is in YAML format and has three main sections:

1. `input`: Defines how to extract data from different file types
2. `output`: Defines the structure of the output data
3. `export`: Defines format-specific export settings

The website provides a complete example of a configuration file that you can download and modify for your specific needs.

## Support and Updates

The website will be updated with new features and improvements to the Text Extractor Tool. Check back regularly for updates.

If you encounter any issues or have questions about using the tool, please refer to the documentation on the website or contact the developer through the GitHub repository.
