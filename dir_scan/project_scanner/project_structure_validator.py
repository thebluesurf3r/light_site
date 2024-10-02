#dir_scan/project_scanner/project_structure_validator.py

import os
import logging
import pandas as pd

from .directory_scanner import scan_directory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#=====================================================================================================================================================#
#== Function to Validate App Structure ==#

def validate_structure(app_name, root_dir):
    """
    Validate the directory structure of a Django app.

    Parameters:
    - app_name (str): The name of the Django app to validate.
    - root_dir (str): The root directory of the Django project.

    Returns:
    - bool: True if the app structure is valid, otherwise False.
    """
    app_path = os.path.join(root_dir, app_name)
    
    # Required files and directories for a valid Django app structure
    required_files = ['__init__.py', 'models.py', 'views.py', 'urls.py']
    required_directories = ['migrations']
    
    # Optional files that are commonly found in Django apps
    optional_files = ['admin.py', 'forms.py', 'tests.py']

    # Check if app directory exists
    if not os.path.isdir(app_path):
        logging.error(f"App directory '{app_path}' does not exist.")
        return False

    # Check for required files
    for file in required_files:
        if not os.path.isfile(os.path.join(app_path, file)):
            logging.error(f"Missing required file '{file}' in app '{app_name}'.")
            return False

    # Check for required directories
    for directory in required_directories:
        if not os.path.isdir(os.path.join(app_path, directory)):
            logging.error(f"Missing required directory '{directory}' in app '{app_name}'.")
            return False

    # Log missing optional files as warnings
    for file in optional_files:
        if not os.path.isfile(os.path.join(app_path, file)):
            logging.warning(f"Optional file '{file}' is missing in app '{app_name}'.")

    logging.info(f"App '{app_name}' structure is valid.")
    return True

# Apply the function to check if files are in the expected location
def validate_app_structure(meta_df, app_name, root_dir):
    """ Validate the structure of the app and log results. """
    is_valid_structure = validate_structure(app_name, root_dir)
    logging.info(f"App '{app_name}' has a valid structure: {is_valid_structure}")

    # Log the result of file location validation
    logging.info("Validating file location for all rows.")
    
    # Assuming check_file_location is defined elsewhere
    meta_df['expected_location'] = meta_df.apply(check_file_location, axis=1)

    # To check counts of valid/invalid locations
    counts = meta_df['expected_location'].value_counts()
    logging.info(f"Counts of expected locations:\n{counts}")