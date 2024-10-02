#dir_scan/visualization_utils/color_map_generator.py

import pandas as pd
import logging
from .models import ProjectEntity

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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