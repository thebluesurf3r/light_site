# dir_scan/views.py

import logging
import os
import re
import pandas as pd
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import ProjectEntity
from .utils import (scan_directories,
                    feature_engineer,
                    display_dataframe_html,
                    categorize_by_extension,
                    categorize_file_extensions,
                    check_file_location,
                    validate_app_structure,
                    generate_custom_hover,
                    create_color_map,
                    export_dataframe,
                    display_dataframe, meta_df)
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
    
    # Load the data from the database
    data = ProjectEntity.objects.all()  # Fetch all entries from the database
    
    # Validate the structure of the 'light_site' app
    app_name = 'dir_scan'
    base_dir = os.path.join(os.path.expanduser('~'), 'git', 'light_site')
    is_valid_structure = validate_app_structure(app_name, base_dir)
    
    if is_valid_structure:
        logger.info(f"App '{app_name}' has a valid structure.")
    else:
        logger.error(f"App '{app_name}' does not have a valid structure.")
    
    # Check if data exists
    if data.exists():
        # Convert QuerySet to DataFrame
        data_df = pd.DataFrame(list(data.values()))  # Create DataFrame from QuerySet
        
        # Drop the specified columns, including 'index' and the 'entity_name'
        exclude_columns = ['hover_template', 'metadata_change_time', 'access_time',
                           'file_age_in_days', 'meta_data_age_in_days', 'python_file',
                           'file_size_category', 'recently_accessed', 'expected_location',
                           'full_path', 'file_depth', 'id', 'entity_name']  # Ensure to exclude 'id' and 'entity_name'
        
        data_df = data_df.drop(columns=exclude_columns, errors='ignore')
        
        search_query = request.GET.get('search', '')
        pattern = re.compile(re.escape(search_query), re.IGNORECASE)

        if search_query:
            data_df = data_df[data_df['filename'].str.contains(search_query, na=False, case=False, regex=True)]

        # Get the count of rows after filtering
        result_count = len(data_df)
        
        # Set up pagination
        paginator = Paginator(data_df, 6)  # Show 6 rows per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Convert DataFrame to HTML table
        table_html = page_obj.object_list.to_html(classes='data table table-bordered table-hover', index=False)
        
        # Pagination controls
        pagination_html = {
            'has_previous': page_obj.has_previous(),
            'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'has_next': page_obj.has_next(),
            'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'page_numbers': range(1, 6),
        }
    else:
        table_html = "<p>No data available</p>"
        pagination_html = {}

    # Pass table and pagination controls to the template
    context = {
        'table_html': table_html,
        'pagination_html': pagination_html,
        'search_query': search_query,
        'result_count': result_count,
    }
    
    return render(request, 'dir_scan/index.html', context)