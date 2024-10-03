#dir_scan/visualization_utils/custom_tooltips.py

import pandas as pd
import logging
from dir_scan.models import ProjectEntity

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#=====================================================================================================================================================#
#== Function to Generate Custom Hover ==#

def generate_custom_hover(row):
    """
    Generate custom hover text for a DataFrame row.

    Parameters:
    - row (pd.Series): A single row of the DataFrame.

    Returns:
    - str: The formatted hover text with file details for Plotly hover templates.
    """
    return (
        f"<b>Entity Name:</b> {row.get('filename', 'N/A')}<br>"
        f"<b>Relative Path:</b> {row.get('directory', 'N/A')}<br>"
        f"<b>Directory Level:</b> {row.get('file_depth', 'N/A')}<br>"
    )

def apply_custom_hover(meta_df):
    """
    Apply the hover template to a DataFrame for use in Plotly visualizations.

    Parameters:
    - meta_df (pd.DataFrame): The DataFrame containing metadata.

    Returns:
    - meta_df (pd.DataFrame): Updated DataFrame with the hover_template column added.
    """
    meta_df['hover_template'] = meta_df.apply(generate_custom_hover, axis=1)
    logging.info("Hover template created and applied to DataFrame.")
    return meta_df
