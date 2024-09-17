# project_structure/views.py
import logging
import os
import re
import pandas as pd
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
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
from django.core.paginator import Paginator
from django.shortcuts import render

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def index(request):
    """
    Render the index page with optional search functionality.
    """
    logger.info('Rendering home page of this app')
    
    # Specify the path to your dataset
    base_dir = os.path.join(os.path.expanduser('~'), 'git', 'light_site')
    file_path = os.path.join(base_dir, 'data', 'project_structure.pkl')
    
    # Load the data
    data = load_data(file_path, drop_na=True, encoding='utf-8')

    if data is not None:
        search_query = request.GET.get('search', '')
        
        # Filter data based on the search query
        if search_query:
            pattern = re.compile(search_query, re.IGNORECASE)
            # Apply regex filter on 'directory_name' or 'entity_name'
            data = data[data.apply(lambda row: pattern.search(row['directory_name']) or pattern.search(row['entity_name']), axis=1)]
        
        # Set up pagination
        paginator = Paginator(data, 10)  # Show 10 rows per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Convert DataFrame to HTML table
        table_html = page_obj.object_list.to_html(classes='data table table-bordered table-hover')
        
        # Pagination controls
        pagination_html = {
            'has_previous': page_obj.has_previous(),
            'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'has_next': page_obj.has_next(),
            'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'page_numbers': range(1, paginator.num_pages + 1),
        }
    else:
        table_html = "<p>No data available</p>"
        pagination_html = {}

    # Pass table and pagination controls to the template
    context = {
        'table_html': table_html,
        'pagination_html': pagination_html,
        'search_query': search_query,  # Pass the search query to the template
    }
    
    return render(request, 'project_structure/index.html', context)



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