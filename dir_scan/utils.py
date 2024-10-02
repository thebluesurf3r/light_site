import re
import os
import time
import logging
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.io as pio
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from queue import Queue
from threading import Thread
from sqlalchemy import create_engine, Table, Column, MetaData, String, DateTime
from django.conf import settings
from logging.handlers import RotatingFileHandler
from light_site.log import log_imported_libraries
from datetime import datetime

from .models import ProjectEntity

from sqlalchemy import create_engine


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#=====================================================================================================================================================#
#== Performing Directory Walk ==#

def scan_directories(root_dir):
    logging.info(f'Starting directory scan of {root_dir}')
    data = []
    total_files = 0

    # Walk through the directory
    for dirpath, dirnames, filenames in os.walk(root_dir):
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

root_dir = os.path.join(os.path.expanduser('~'), 'git', 'light_site')
meta_df = scan_directories(root_dir)

#=====================================================================================================================================================#
#== Feature Engineering ==#

def feature_engineer(meta_df):
    logging.info('Starting feature engineering on the dataset')

    # Feature 1: File age in days
    try:
        logging.info('Applying Feature 1: File age in days based on modification time')
        meta_df['file_age_in_days'] = (datetime.now() - meta_df['modification_time']).dt.days
    except Exception as e:
        logging.error(f'Error while calculating file age in days: {e}')
    
    # Feature 2: Metadata change age in days
    try:
        logging.info('Applying Feature 2: Metadata change age in days')
        meta_df['meta_data_age_in_days'] = (datetime.now() - meta_df['metadata_change_time']).dt.days
    except Exception as e:
        logging.error(f'Error while calculating metadata change age in days: {e}')

    # Feature 3: Recently accessed (less than 3 days)
    try:
        logging.info('Applying Feature 3: Recently accessed files (less than 3 days)')
        meta_df['recently_accessed'] = (datetime.now() - meta_df['access_time']).dt.days < 3
    except Exception as e:
        logging.error(f'Error while determining recently accessed files: {e}')

    # Function to categorize file size
    def categorize_file_size(size):
        try:
            if size < 10**4:  # less than 10KB
                return 'Small'
            elif size < 10**6:  # less than 1MB
                return 'Medium'
            else:
                return 'Large'
        except Exception as e:
            logging.error(f'Error while categorizing file size: {e}')
            return 'Unknown'

    # Feature 4: File size category
    try:
        logging.info('Applying Feature 4: Categorizing file sizes')
        meta_df['file_size_category'] = meta_df['file_size'].apply(categorize_file_size)
    except Exception as e:
        logging.error(f'Error while applying file size categorization: {e}')
    
    # Feature 5: File extension
    try:
        logging.info('Applying Feature 5: Extracting file extensions')
        def extract_file_extension(filename):
            # Extract file extension (without dot) or return 'no_extension' if none is found
            file_extension = os.path.splitext(filename)[1][1:]  # Get the extension without the dot
            if file_extension == '':  # If no extension is found
                return 'no_extension'
            return file_extension
        meta_df['file_extension'] = meta_df['filename'].apply(extract_file_extension)
    except Exception as e:
        logging.error(f'Error while extracting file extensions: {e}')

    # Feature 6: Is Python file
    try:
        logging.info('Applying Feature 6: Identifying Python files')
        meta_df['python_file'] = meta_df['file_extension'] == 'py'
    except Exception as e:
        logging.error(f'Error while identifying Python files: {e}')

    # Feature 7: File depth level by counting slashes in 'full_path'
    try:
        logging.info("Applying Feature 7: Calculating file depth level based on 'full_path'")
        
        # Function to calculate the depth level by counting slashes
        def calculate_depth(full_path):
            return full_path.count('/')  # Count the number of slashes
        
        # Apply the function to the 'full_path' column to create a new 'file_depth' column
        meta_df['file_depth'] = meta_df['full_path'].apply(calculate_depth).astype(int)
    
    except Exception as e:
        logging.error(f"Error while calculating file depth level: {e}")

    logging.info('Feature engineering completed successfully')
    
    return meta_df


# Apply the feature engineering function to meta_df
meta_df = feature_engineer(meta_df)

#=====================================================================================================================================================#
#== Django Element Type ==#

def classify_django_element(file_path, filename):
    # Combine the directory and filename for classification
    full_path = os.path.join(file_path, filename)
    
    # Project-level configuration files
    if 'manage.py' in full_path:
        return 'Django Management Script'
    elif 'settings.py' in full_path or 'urls.py' in full_path or 'wsgi.py' in full_path or 'asgi.py' in full_path:
        return 'Django Project Configuration'

    # App-level files
    elif 'models.py' in full_path:
        return 'Django App Models'
    elif 'views.py' in full_path:
        return 'Django App Views'
    elif 'admin.py' in full_path:
        return 'Django App Admin'
    elif 'apps.py' in full_path:
        return 'Django App Configuration'
    elif 'tests.py' in full_path:
        return 'Django App Tests'
    
    # Migrations
    elif 'migrations/' in full_path and full_path.endswith('.py'):
        return 'Django Migrations'

    # Static files
    elif 'static/' in full_path:
        if filename.endswith('.css'):
            return 'Static CSS File'
        elif filename.endswith('.js'):
            return 'Static JS File'
        elif filename.endswith(('.jpg', '.png', '.gif', '.svg')):
            return 'Static Image File'
        else:
            return 'Other Static File'

    # Templates
    elif 'templates/' in full_path and filename.endswith('.html'):
        return 'Django Template'

    # Log files
    elif filename.endswith('.log'):
        return 'Log File'

    # Environment or dependency files
    elif filename in ['.env', 'Pipfile', 'Pipfile.lock', 'requirements.txt']:
        return 'Environment/Dependency File'
    
    # Other Python files
    elif filename.endswith('.py'):
        return 'Python Script'

    # Default fallback
    return 'Other'

# Apply the classification function to each row
meta_df['django_element_type'] = meta_df.apply(
    lambda row: classify_django_element(row['directory'], row['filename']), axis=1
)

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

def categorize_file_extensions(file_extension):
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

# Example usage:
file_extensions = ['py', 'csv', 'log', 'otf', 'unknown_extension']
categorized = [categorize_file_extensions(ext) for ext in file_extensions]

#=====================================================================================================================================================#
#== Function to Check File Location ==#

def check_file_location(row):
    """
    Check if a file's extension corresponds to its expected location in a Django project.

    Parameters:
    row (pd.Series): A row from the DataFrame containing 'directory' and 'file_extension'.

    Returns:
    bool: True if the file is in the expected location, otherwise False.
    """
    file_extension = row['file_extension'].lower()  # Convert to lowercase for consistency
    directory = row['directory'].lower()  # Convert to lowercase for consistency

    # Define file extensions and their expected locations
    static_extensions = ['css', 'js', 'png', 'jpg', 'jpeg', 'gif', 'svg', 'pdf', 'csv']
    html_extensions = ['html']
    markdown_extensions = ['md', 'rst']
    config_extensions = ['cfg', 'json', 'env', 'ini']
    notebook_extensions = ['ipynb']
    allowed_extensions = static_extensions + html_extensions + markdown_extensions + config_extensions + notebook_extensions

    # Check if file extension is one of the allowed types
    if file_extension in html_extensions and 'templates/' in directory:
        return True
    elif file_extension in static_extensions and 'static/' in directory:
        return True
    elif file_extension == 'py' and (
        'migrations/' in directory or 
        'management/commands/' in directory or 
        'apps/' in directory or
        'admin/' in directory):
        return True
    elif file_extension in config_extensions and (directory.startswith('.') or 'config/' in directory):
        return True
    elif file_extension in markdown_extensions and directory in ['README.md', 'LICENSE']:
        return True
    elif file_extension in notebook_extensions and ('notebooks/' in directory or directory.endswith('.ipynb')):
        return True
    elif file_extension not in allowed_extensions and 'static/' in directory:
        return True

    return False

#=====================================================================================================================================================#
#== Function to Validate App Structure ==#

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
meta_df['expected_location'] = meta_df.apply(check_file_location, axis=1)

# Validate the structure of the 'light_site' app (or any other app name)
app_name = 'light_site'
root_dir = '/home/tron/git/light_site'  # Update this path to your Django project root
is_valid_structure = validate_app_structure(app_name, root_dir)
logging.info(f"App '{app_name}' has a valid structure: {is_valid_structure}")

# Log the result of file location validation
logging.info(f"Validating file location for all rows.")

# To check counts of valid/invalid locations
counts = meta_df['expected_location'].value_counts()
logging.info(f"Checking expected locations for static content")

#=====================================================================================================================================================#
#== Function to Generate Custom Hover ==#

def generate_custom_hover(row):
    """
    Generate custom hover text for a DataFrame row.

    Parameters:
    - row (pd.Series): A single row of the DataFrame.

    Returns:
    - str: The formatted hover text.
    """    
    return (
        f"Entity Name: {row.get('filename', 'N/A')}<br>"
        f"Relative Path: {row.get('directory', 'N/A')}<br>"
        f"Directory Level: {row.get('file_depth', 'N/A')}<br>"
    )

# Apply the function to generate hover text
meta_df['hover_template'] = meta_df.apply(generate_custom_hover, axis=1)
logging.info(f"Hover template created and applied to DataFrame.")

#=====================================================================================================================================================#

# GRAPHS MOVED FROM HERE to plotly_utils.py #

#=====================================================================================================================================================#
#== Function to Export DataFrame ==#

def export_dataframe(meta_df, pickle_file_path):
    """
    Export a DataFrame to both a pickle file and a CSV file.

    Parameters:
    meta_df (pd.DataFrame): The DataFrame to export.
    pickle_file_path (str): The file path where the pickle file will be saved.
    csv_file_path (str): The file path where the CSV file will be saved.
    """
    # Export to pickle file
    meta_df.to_pickle(pickle_file_path)
    logging.info(f"DataFrame exported successfully: {pickle_file_path}")


# Assume meta_df is your DataFrame
file_name = 'structure_processed.pkl' 
pickle_file_path = os.path.join(os.path.expanduser('~'), 'git', 'light_site', 'media', 'dir_scan', 'pkl', file_name)

export_dataframe(meta_df, pickle_file_path)

#=====================================================================================================================================================#
#== Function to Create Color Map ==#

def create_color_map(meta_df, category_column):
    """
    Create a color map for unique values in a specified column.

    Parameters:
    meta_df (pd.DataFrame): The DataFrame containing the data.
    category_column (str): The column name with categorical data.

    Returns:
    color_discrete_map (dict): A dictionary mapping unique categories to colors.
    """
    unique_values_list = meta_df[category_column].unique().tolist()

    # Ensure that there are enough colors by repeating the Jet palette if needed
    color_map = px.colors.sequential.Jet * (len(unique_values_list) // len(px.colors.sequential.Jet) + 1)
    color_discrete_map = dict(zip(unique_values_list, color_map[:len(unique_values_list)]))
    
    return color_discrete_map
    
#=====================================================================================================================================================#
#== Display DataFrame in HTML Function ==#

def display_dataframe_html(rows=5, exclude_column='hover_template'):
    """
    Render a preview of the DataFrame from the database as an HTML table, excluding a specified column.

    Parameters:
    - rows: int, number of rows to display (default: 5)
    - exclude_column: str, name of the column to exclude (default: 'hover_template')

    Returns:
    - str: HTML table representing the DataFrame sample
    """
    logging.info(f"Rendering an HTML preview of the DataFrame, showing the first {rows} rows.")
    
    # Fetch data from the database
    meta_df = pd.DataFrame(list(ProjectEntity.objects.values()))  # Create DataFrame from QuerySet

    # Exclude the specified column if it exists
    if exclude_column in meta_df.columns:
        meta_df = meta_df.drop(columns=exclude_column)
        logging.info(f"Excluded column: {exclude_column}")

    # Select the first few rows for preview
    meta_df_sample = meta_df.head(rows)

    # Return the DataFrame as an HTML table
    return meta_df_sample.to_html(classes="table table-striped", index=False)

#=====================================================================================================================================================#
#== Function to Display DataFrame ==#

def display_dataframe(rows=5, exclude_column='hover_template'):
    """
    Return a preview of the DataFrame from the database.

    Parameters:
    - rows: int, number of rows to display (default: 5)
    - exclude_column: str, name of the column to exclude (default: 'hover_template')

    Returns:
    - pd.DataFrame: Sample of the DataFrame
    """
    logging.info("Previewing the dataset.")

    # Fetch data from the database
    meta_df = pd.DataFrame(list(ProjectEntity.objects.values()))  # Create DataFrame from QuerySet

    # Exclude the specified column if it exists
    if exclude_column in meta_df.columns:
        meta_df = meta_df.drop(columns=exclude_column)

    # Return the first few rows
    return meta_df.head(rows)

# Example usage
preview_data = display_dataframe(rows=10)

#=====================================================================================================================================================#
#== Function to push dataFrame to database ==#

def push_dataframe_to_db(df, table_name, db_url):
    """
    Push a Pandas DataFrame to a PostgreSQL database table.

    Args:
    df (pd.DataFrame): The DataFrame to push.
    table_name (str): The target table name in the PostgreSQL database.
    db_url (str): The database URL connection string.

    Returns:
    bool: True if successful, False otherwise.
    """
    try:
        # Create database engine
        engine = create_engine(db_url)
        logging.info(f'Connection established to the database: {db_url}')
        
        # Push DataFrame to the table
        df.to_sql(table_name, con=engine, if_exists='append', index=False)
        logging.info(f'Successfully inserted data into table: {table_name}')

        return True

    except SQLAlchemyError as e:
        # Log the error if something goes wrong
        logging.error(f"Error inserting data into table {table_name}: {str(e)}")
        return False

    except Exception as e:
        # Catch any other exceptions
        logging.error(f"Unexpected error: {str(e)}")
        return False


db_url = "postgresql+psycopg2://postgres:password@localhost:5432/job_applications"
if push_dataframe_to_db(meta_df, 'project_structure_projectentity', db_url):
    logging.info("Data successfully pushed to the database.")
else:
    logging.info("Failed to push data to the database.")