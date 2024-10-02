#dir_scan/project_scanner/directory_scanner.py

import os
import logging
import pandas as pd
from datetime import datetime

from .file_categorizer import categorize_file
from .project_structure_validator import validate_structure

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#=====================================================================================================================================================#
#== Performing Directory Scan ==#

def scan_directories(root_dir):
    logging.info(f'Starting directory scan of {root_dir}')
    data = []
    total_files = 0

    # Walk through the directory
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                file_stats = os.stat(file_path)
                
                # Collect file metadata
                file_size = file_stats.st_size
                metadata_change_time = datetime.fromtimestamp(file_stats.st_ctime)
                modification_time = datetime.fromtimestamp(file_stats.st_mtime)
                access_time = datetime.fromtimestamp(file_stats.st_atime)

                # Append metadata to the list
                data.append({
                    'directory': dirpath,
                    'filename': filename,
                    'full_path': file_path,
                    'file_size': file_size,
                    'metadata_change_time': metadata_change_time,
                    'modification_time': modification_time,
                    'access_time': access_time
                })
                total_files += 1

            except FileNotFoundError:
                logging.error(f'File not found: {file_path}')
            except PermissionError:
                logging.error(f'Permission denied for file: {file_path}')
            except Exception as e:
                logging.error(f'Error processing file {filename} in directory {dirpath}: {e}')

    # Convert to a pandas DataFrame with appropriate columns
    df = pd.DataFrame(data)
    logging.info(f'Scanning completed. Total files processed: {total_files}')
    
    return df
