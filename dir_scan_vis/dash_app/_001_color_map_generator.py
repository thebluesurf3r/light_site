#dir_scan/visualization_utils/color_map_generator.py

import pandas as pd
import logging
from dir_scan.models import ProjectEntity
import plotly.express as px

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

meta_df = ProjectEntity.objects.all()

#=====================================================================================================================================================#
#== Function to Create Color Map ==#

def create_color_map(meta_df, category_column):
    """
    Create a color map for unique values in a specified column.

    Parameters:
    - meta_df (pd.DataFrame): The DataFrame containing the data.
    - category_column (str): The column name with categorical data.

    Returns:
    - color_discrete_map (dict): A dictionary mapping unique categories to colors.
    """
    # Handle case where category_column may not exist
    if category_column not in meta_df.columns:
        logger.error(f"Column '{category_column}' does not exist in the DataFrame.")
        return {}

    unique_values_list = meta_df[category_column].unique().tolist()

    # Ensure there are enough colors by repeating the Jet palette if needed
    color_map = px.colors.sequential.Jet * (len(unique_values_list) // len(px.colors.sequential.Jet) + 1)
    color_discrete_map = dict(zip(unique_values_list, color_map[:len(unique_values_list)]))

    logging.info(f"Color map generated for column '{category_column}' with {len(unique_values_list)} unique values.")
    return color_discrete_map
