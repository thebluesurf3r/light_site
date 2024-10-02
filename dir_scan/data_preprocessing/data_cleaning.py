#dir_scan/data_preprocessing/data_cleaning.py

# Standard imports
import logging
import pandas as pd

# Local imports
from .models import ProjectEntity

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#=====================================================================================================================================================#
#== Data Cleaning ==#

def clean_data(meta_df):
    """
    Cleans the dataset by handling missing values, removing duplicates, and correcting data types.

    Parameters:
    - meta_df (pd.DataFrame): The DataFrame containing file metadata and features.

    Returns:
    - pd.DataFrame: The cleaned DataFrame.
    """
    logging.info('Starting data cleaning process')

    # Make a copy of the DataFrame to avoid modifying the original data
    cleaned_df = meta_df.copy()

    # 1. Handle missing values
    try:
        # Fill missing file sizes with 0
        cleaned_df['file_size'].fillna(0, inplace=True)
        
        # Fill missing modification times with a placeholder (e.g., current time)
        cleaned_df['modification_time'].fillna(pd.Timestamp.now(), inplace=True)

        # Fill missing access times with current time as a placeholder
        cleaned_df['access_time'].fillna(pd.Timestamp.now(), inplace=True)

        # Optionally, you can drop rows where essential columns are NaN
        # cleaned_df.dropna(subset=['filename', 'full_path'], inplace=True)

        logging.info('Missing values handled successfully')
    except Exception as e:
        logging.error(f'Error while handling missing values: {e}')

    # 2. Remove duplicates
    try:
        initial_count = cleaned_df.shape[0]
        cleaned_df.drop_duplicates(subset=['full_path'], inplace=True)
        final_count = cleaned_df.shape[0]
        logging.info(f'Duplicates removed: {initial_count - final_count}')
    except Exception as e:
        logging.error(f'Error while removing duplicates: {e}')

    # 3. Correct data types if necessary
    try:
        cleaned_df['file_size'] = cleaned_df['file_size'].astype(int)
        cleaned_df['modification_time'] = pd.to_datetime(cleaned_df['modification_time'])
        cleaned_df['access_time'] = pd.to_datetime(cleaned_df['access_time'])

        logging.info('Data types corrected successfully')
    except Exception as e:
        logging.error(f'Error while correcting data types: {e}')

    logging.info('Data cleaning process completed successfully')
    
    return cleaned_df

meta_df = clean_data(meta_df)
