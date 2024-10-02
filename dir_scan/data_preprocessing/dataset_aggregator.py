#dir_scan/data_preprocessing/dataset_aggregator.py

# Standard imports
import logging
import pandas as pd

# Local imports
from .data_cleaning import clean_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def aggregate_dataset(meta_df):
    """
    Aggregates and summarizes the dataset from the directory scan.

    Parameters:
    - meta_df (pd.DataFrame): The DataFrame containing file metadata and features.

    Returns:
    - dict: A dictionary containing various aggregation metrics.
    """
    logging.info('Starting dataset aggregation')

    try:
        # Total number of files
        total_files = meta_df.shape[0]

        # Total size of files
        total_size = meta_df['file_size'].sum()

        # Average file size
        avg_size = meta_df['file_size'].mean()

        # Count of files by category
        file_size_counts = meta_df['file_size_category'].value_counts().to_dict()
        
        # Count of Python files
        python_file_count = meta_df['python_file'].sum()

        # Count of recently accessed files
        recently_accessed_count = meta_df['recently_accessed'].sum()

        # Prepare the aggregated results
        aggregated_results = {
            'total_files': total_files,
            'total_size': total_size,
            'average_file_size': avg_size,
            'file_size_distribution': file_size_counts,
            'python_file_count': python_file_count,
            'recently_accessed_count': recently_accessed_count
        }

        logging.info('Dataset aggregation completed successfully')
        return aggregated_results

    except Exception as e:
        logging.error(f'Error during dataset aggregation: {e}')
        return {}

meta_df = aggregate_dataset(meta_df)
