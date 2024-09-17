import re
import os
import time
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from django.conf import settings
from light_site.log import log_imported_libraries
from logging.handlers import RotatingFileHandler
from queue import Queue
from threading import Thread

#=====================================================================================================================================================#

# Global DataFrame to store log entries
log_df = pd.DataFrame(columns=['Timestamp', 'Level', 'Message'])

class DataFrameLoggingHandler(logging.Handler):
    def __init__(self, dataframe, queue):
        super().__init__()
        self.dataframe = dataframe
        self.queue = queue

    def emit(self, record):
        try:
            timestamp = pd.Timestamp.now()
            level = record.levelname
            message = record.getMessage()
            self.queue.put((timestamp, level, message))
        except Exception:
            self.handleError(record)

def process_log_queue(dataframe, queue):
    while True:
        while not queue.empty():
            timestamp, level, message = queue.get()
            dataframe.loc[len(dataframe)] = [timestamp, level, message]

def setup_logging(log_file='app_log.log', log_level=logging.INFO):
    """
    Set up logging configuration to log to a file and console, and return a logger.
    """
    logging.root.handlers.clear()

    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Define handlers
    log_queue = Queue()
    handlers = [
        RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5),  # 10 MB per file
        logging.StreamHandler(),
        DataFrameLoggingHandler(log_df, log_queue)  # Provide both arguments here
    ]
    
    for handler in handlers:
        handler.setLevel(log_level)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)

    # Start a thread to process the log queue
    log_thread = Thread(target=process_log_queue, args=(log_df, log_queue), daemon=True)
    log_thread.start()

    return logger

# Usage
logger = setup_logging(log_file='app_log.log', log_level=logging.INFO)
libraries_with_aliases = {
    'os': None,
    'time': None,
    're': 're',
    'pandas': 'pd',
    'numpy': 'np',
    'matplotlib.pyplot': 'plt',
    'seaborn': 'sns',
    'plotly.express': 'px',
    'plotly.graph_objects': 'go',
    'plotly.io': 'pio'
}
logger.info("Initializing logging configuration")

base_dir = os.path.join(os.path.expanduser('~'), 'git', 'light_site')

file_path = os.path.join(base_dir, 'data', 'project_structure.pkl')
drop_na = False
encoding = False

#=====================================================================================================================================================#

def load_data(file_path, drop_na=False, encoding='utf-8'):
    """
    Load a dataset from a pickle file, with optional date parsing and NaN removal.

    Parameters:
    - file_path: str, path to the dataset
    - drop_na: bool, drop rows with NaN values (default: True)
    - encoding: str, file encoding type (default: 'utf-8')

    Returns:
    - pd.DataFrame: The loaded dataset or None if an error occurred
    """
    try:
        df = pd.read_pickle(file_path)
        logging.info(f"Dataset loaded successfully from: {file_path}")

        if drop_na:
            initial_rows = df.shape[0]
            df.dropna(inplace=True)
            removed_rows = initial_rows - df.shape[0]
            logging.info(f"Removed {removed_rows} rows with NaN values.")

        df.reset_index(drop=True, inplace=True)
        logging.info("Index reset.")

        return df

    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except pd.errors.EmptyDataError:
        logging.error(f"No data found in file: {file_path}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

#=====================================================================================================================================================#

# Load the dataset using load_data
df = load_data(file_path=file_path, drop_na=drop_na, encoding=encoding)

#=====================================================================================================================================================#

# Check if the DataFrame was successfully loaded
if df is not None:
    logging.info(f"Dataset loaded with {df.shape[0]} rows and {df.shape[1]} columns.")

def display_dataframe_html(df, rows=5, exclude_column='hover_template'):
    """
    Render a preview of the DataFrame as an HTML table, excluding a specified column.

    Parameters:
    - df: pd.DataFrame, the DataFrame to display
    - rows: int, number of rows to display (default: 5)
    - exclude_column: str, name of the column to exclude (default: 'hover_template')

    Returns:
    - str: HTML table representing the DataFrame sample
    """
    logging.info(f"Rendering an HTML preview of the DataFrame, showing the first {rows} rows.")
    
    # Exclude the specified column if it exists
    if exclude_column in df.columns:
        df = df.drop(columns=[exclude_column])
        logging.info(f"Excluded column: {exclude_column}")

    # Select the first few rows for preview
    df_sample = df.head(rows)

    # Return the DataFrame as an HTML table
    return df_sample.to_html(classes="table table-striped", index=False)

# Display the DataFrame as an HTML table
html_table = display_dataframe_html(df, rows=5)

#=====================================================================================================================================================#

def categorize_by_extension(df):
    """
    Extract and categorize file extensions from the 'entity_name' column.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the data.

    Returns:
    - pd.DataFrame: DataFrame with an additional 'file_extension' column.
    """
    try:
        logging.info("Categorizing data by file extension.")

        # Apply the categorization by extracting the file extension
        df['file_extension'] = df['entity_name'].apply(lambda x: x.split('.')[-1] if '.' in x else 'No Extension')

        # Log the unique file extensions found
        unique_extensions = df['file_extension'].unique()
        logging.info(f"Found {len(unique_extensions)} unique file extensions: {unique_extensions}")

        return df

    except Exception as e:
        logging.error(f"An error occurred while categorizing file extensions: {e}")
        raise

# Apply the function to categorize file extensions
df = categorize_by_extension(df)

#=====================================================================================================================================================#

def check_file_location(row):
    """
    Check if a file's extension corresponds to its expected location in a Django project.

    Parameters:
    row (pd.Series): A row from the DataFrame containing 'relative_path' and 'file_extension'.

    Returns:
    bool: True if the file is in the expected location, otherwise False.
    """
    file_extension = row['file_extension'].lower()  # Convert to lowercase for consistency
    relative_path = row['relative_path'].lower()  # Convert to lowercase for consistency

    # Define file extensions and their expected locations
    static_extensions = ['css', 'js', 'png', 'jpg', 'jpeg', 'gif', 'svg', 'pdf', 'csv']
    html_extensions = ['html']
    markdown_extensions = ['md', 'rst']
    config_extensions = ['cfg', 'json', 'env', 'ini']
    notebook_extensions = ['ipynb']
    allowed_extensions = static_extensions + html_extensions + markdown_extensions + config_extensions + notebook_extensions

    # Check if file extension is one of the allowed types
    if file_extension in html_extensions and 'templates/' in relative_path:
        return True
    elif file_extension in static_extensions and 'static/' in relative_path:
        return True
    elif file_extension == 'py' and (
        'migrations/' in relative_path or 
        'management/commands/' in relative_path or 
        'apps/' in relative_path or
        'admin/' in relative_path):
        return True
    elif file_extension in config_extensions and (relative_path.startswith('.') or 'config/' in relative_path):
        return True
    elif file_extension in markdown_extensions and relative_path in ['README.md', 'LICENSE']:
        return True
    elif file_extension in notebook_extensions and ('notebooks/' in relative_path or relative_path.endswith('.ipynb')):
        return True
    elif file_extension not in allowed_extensions and 'static/' in relative_path:
        return True

    return False

#=====================================================================================================================================================#

def validate_app_structure(app_name, root_dir):
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

# Logging the function usage
logging.info(f"Validating app structure: {validate_app_structure}")

# Apply the function to check if files are in the expected location
df['expected_location'] = df.apply(check_file_location, axis=1)

# Validate the structure of the 'light_site' app (or any other app name)
app_name = 'light_site'
root_dir = '/home/tron/git/light_site'  # Update this path to your Django project root
is_valid_structure = validate_app_structure(app_name, root_dir)
logging.info(f"App '{app_name}' has a valid structure: {is_valid_structure}")

# Log the result of file location validation
logging.info(f"Validating file location for all rows.")

# To check counts of valid/invalid locations
counts = df['expected_location'].value_counts()
logging.info(f"Counts of expected locations: {counts}")

#=====================================================================================================================================================#

def generate_custom_hover(row):
    """
    Generate custom hover text for a DataFrame row.

    Parameters:
    - row (pd.Series): A single row of the DataFrame.

    Returns:
    - str: The formatted hover text.
    """    
    return (
        f"Directory Name: {row.get('directory_name', 'N/A')}<br>"
        f"Entity Name: {row.get('entity_name', 'N/A')}<br>"
        f"Relative Path: {row.get('relative_path', 'N/A')}<br>"
        f"Directory Level: {row.get('directory_level_count', 'N/A')}<br>"
        f"Type: {row.get('type', 'N/A')}<br>"
    )

# Apply the function to generate hover text
df['hover_template'] = df.apply(generate_custom_hover, axis=1)
logging.info(f"Hover template created and applied to DataFrame.")


#=====================================================================================================================================================#

def create_color_map(df, category_column):
    """
    Create a color map for unique values in a specified column.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    category_column (str): The column name with categorical data.

    Returns:
    color_discrete_map (dict): A dictionary mapping unique categories to colors.
    """
    unique_values_list = df[category_column].unique().tolist()

    # Ensure that there are enough colors by repeating the Jet palette if needed
    color_map = px.colors.sequential.Jet * (len(unique_values_list) // len(px.colors.sequential.Jet) + 1)
    color_discrete_map = dict(zip(unique_values_list, color_map[:len(unique_values_list)]))
    
    return color_discrete_map

#=====================================================================================================================================================#

# GRAPHS MOVED FROM HERE to plotly_utils.py #

#=====================================================================================================================================================#

def export_dataframe(df, pickle_file_path, csv_file_path):
    """
    Export a DataFrame to both a pickle file and a CSV file.

    Parameters:
    df (pd.DataFrame): The DataFrame to export.
    pickle_file_path (str): The file path where the pickle file will be saved.
    csv_file_path (str): The file path where the CSV file will be saved.
    """
    # Export to pickle file
    df.to_pickle(pickle_file_path)
    logging.info(f"DataFrame exported successfully: {pickle_file_path}")

    # Export to CSV file
    df.to_csv(csv_file_path, index=False)
    logging.info(f"DataFrame exported successfully: {csv_file_path}")


# Assume df is your DataFrame
pickle_path = 'structure_processed.pkl'
csv_path = 'structure_processed.csv'

export_dataframe(df, pickle_path, csv_path)

#=====================================================================================================================================================#

def display_dataframe(df, rows=5, exclude_column='hover_template'):
    logging.info(f"Previewing the dataset: {display_dataframe}")
    if exclude_column in df.columns:
        df = df.drop(columns=exclude_column)
    return df.head(rows)

preview_data = display_dataframe(df, rows=10)
preview_data

#=====================================================================================================================================================#

logging.info(f"Log size: {log_df.shape}")

def display_log_df(log_df, rows=5, exclude_column=None):
    logging.info(f"Viewing the log: {display_dataframe}")
    if exclude_column in df.columns:
        log_df = log_df.drop(columns=exclude_column)
    return log_df.head(rows)

preview_log = display_log_df(log_df, rows=20)
preview_log

#=====================================================================================================================================================#