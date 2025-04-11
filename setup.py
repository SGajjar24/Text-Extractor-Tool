"""
Setup script for the Text Extractor tool.
"""
from setuptools import setup, find_packages

setup(
    name="text_extractor",
    version="0.1.0",
    description="A tool to extract data from unorganized files and export to multiple formats",
    author="Manus AI",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0",
        "openpyxl>=3.0.7",
        "python-docx>=0.8.11",
        "pyyaml>=6.0",
        "click>=8.0.0",
        "xlrd>=2.0.1",
    ],
    entry_points={
        "console_scripts": [
            "text-extractor=text_extractor.src.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
)
