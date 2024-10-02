#dir_scan/display_utils/dataframe_printer.py

import pandas as pd
import logging
from .models import ProjectEntity

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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