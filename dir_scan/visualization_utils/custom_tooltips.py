#dir_scan/visualization_utils/custom_tooltips.py

import pandas as pd
import logging
from .models import ProjectEntity

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