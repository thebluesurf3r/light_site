#dir_scan/project_scanner/file_categorizer.py

import re
import os
import logging
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from django.conf import settings

from .directory_scanner import scan_directory
from light_site.log import log_imported_libraries

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#=====================================================================================================================================================#
#== Categorize Data by Extension ==#

def categorize_by_extension(meta_df):
    """
    Extract and categorize file extensions from the 'filename' column.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the data.

    Returns:
    - pd.DataFrame: DataFrame with an additional 'file_extension' column.
    """
    try:
        logging.info("Categorizing data by file extension.")

        # Apply the categorization by extracting the file extension
        meta_df['file_extension'] = meta_df['filename'].apply(lambda x: x.split('.')[-1] if '.' in x else 'No Extension')

        # Log the unique file extensions found
        unique_extensions = meta_df['file_extension'].unique()
        logging.info(f"Found {len(unique_extensions)} unique extensions.")

        return meta_df

    except Exception as e:
        logging.error(f"An error occurred while categorizing file extensions: {e}")
        raise

# Apply the function to categorize file extensions
meta_df = categorize_by_extension(meta_df)

#=====================================================================================================================================================#
#== Categorize the Extracted Extensions ==#

def categorize_file(file_extension):
    # Define file extension categories
    buckets = {
        "Code Files": ['py', 'ipynb', 'js', 'ts', 'mjs', 'mts', 'cjs', 'php', 'cts'],
        "Data Files": ['csv', 'pkl', 'sqlite3', 'xml', 'json'],
        "Configuration Files": ['env', 'gitignore', 'yml', 'lock', 'cfg', 'eslintrc', 'nycrc', 'babelrc', 'jshintrc', 'npmignore'],
        "Text Files": ['txt', 'md', 'markdown', '1', '10'],
        "Log Files": ['log', 'history'],
        "Web Files": ['html', 'css', 'scss', 'svg', 'webmanifest'],
        "Font Files": ['otf', 'ttf'],
        "Image Files": ['png', 'jpg'],
        "Executable Files": ['exe'],
        "Other": ['No Extension', 'enc', 'git', 'closure-compiler', 'esprima', 'BSD', 'bin', 'def', 'tmpl', 'dist-info', 'pth', 'pem'],
        "Miscellaneous": ['sample', 'realpath', 'merge', 'walk', 'scandir', 'stat', 'vite', 'applescript', 'ps1', 'csh', 'fish'],
    }
    
    # Loop through buckets and categorize file extension
    for category, extensions in buckets.items():
        if file_extension in extensions:
            return category
    return "Unknown"  # For any uncategorized file extensions

file_extensions = ['py', 'csv', 'log', 'otf', 'unknown_extension']
categorized = [categorize_file(ext) for ext in file_extensions]