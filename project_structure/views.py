# project_structure/views.py
import logging
import os
import pandas as pd
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from .utils import (setup_logging,
                    log_imported_libraries,
                    load_data,
                    display_dataframe_html,
                    categorize_by_extension,
                    check_file_location,
                    validate_app_structure,
                    generate_custom_hover,
                    create_color_map,
                    export_dataframe,
                    display_dataframe,
                    display_log_df)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def index(request):
    """
    Render the index page.
    """
    logger.info('Rendering home page of this app')
    return render(request, 'project_structure/index.html')



def graphs(request):
    """
    Load data, process it, and render the graphs page.
    """

    logger.info('Received request for graphs page')

    try:
        # Parameters
        file_name = 'project_structure.pkl'
        file_path = os.path.join(settings.BASE_DIR, 'media', 'project_structure', 'data', file_name)
        drop_na = True   # Whether to drop rows with NaN values
        encoding = 'utf-8'  # Encoding format

        logger.info(f'Attempting to load data from file: {file_path}')
        
        # Load the dataset using load_data
        df = load_data(file_path=file_path, drop_na=drop_na, encoding=encoding)
        
        if df is None:
            raise ValueError("DataFrame is None, which indicates an issue with loading the data.")
        
        logger.info('Data loaded successfully')

        # Limit DataFrame to 10 rows
        df_limited = df.head(10)
    
        # Convert limited DataFrame to HTML
        df_html = df_limited.to_html(classes='data', header=True, index=False)
    
        # Context for template
        context = {
            'df_html': df_html
        }

    except FileNotFoundError as e:
        logger.error(f'File not found: {e}')
        context = {'error': 'Data not available.'}
    except ValueError as e:
        logger.error(f'Value error: {e}')
        context = {'error': 'Data not available.'}
    except Exception as e:
        logger.error(f'An unexpected error occurred: {e}')
        context = {'error': 'Data not available.'}

    # Pass the data to the template
    logger.info('Rendering graphs page')
    return render(request, 'project_structure/graphs.html', context)