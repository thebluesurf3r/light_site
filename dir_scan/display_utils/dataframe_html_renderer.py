#dir_scan/display_utils/dataframe_html_renderer.py

import pandas as pd
import logging

from .models import ProjectEntity
from .dataframe_printer import print_dataframe

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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