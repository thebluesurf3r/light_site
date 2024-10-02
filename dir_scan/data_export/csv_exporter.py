#dir_scan/data_export/csv_exporter.py

import os
import logging
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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