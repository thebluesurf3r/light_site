#dir_scan/data_preprocessing/feature_engineering.py

# Standard imports
import os
import logging
from datetime import datetime

# Local imports
from .dataset_aggregator import aggregate_dataset
from .data_cleaning import clean_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        """Categorizes file size into Small, Medium, or Large."""
        if size < 10**4:  # less than 10KB
            return 'Small'
        elif size < 10**6:  # less than 1MB
            return 'Medium'
        else:
            return 'Large'

    # Feature 4: File size category
    try:
        logging.info('Applying Feature 4: Categorizing file sizes')
        meta_df['file_size_category'] = meta_df['file_size'].apply(categorize_file_size)
    except Exception as e:
        logging.error(f'Error while applying file size categorization: {e}')
    
    # Feature 5: File extension
    try:
        logging.info('Applying Feature 5: Extracting file extensions')
        meta_df['file_extension'] = meta_df['filename'].apply(lambda x: os.path.splitext(x)[1][1:] or 'no_extension')
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
        meta_df['file_depth'] = meta_df['full_path'].apply(lambda x: x.count('/')).astype(int)
    except Exception as e:
        logging.error(f"Error while calculating file depth level: {e}")

    logging.info('Feature engineering completed successfully')
    
    return meta_df

meta_df = feature_engineer(meta_df)
