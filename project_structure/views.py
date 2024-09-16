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
import os
import pandas as pd
from django.conf import settings

def index(request):
    """
    Data processing functions from utils.py
    """
    return render(request, 'project_structure/index.html')

def graphs(request):
    # Load your data here, for example, from a pickle file
    try:
        # Parameters provided from outside the function
        file_name = 'project_structure.pkl'
        file_path = os.path.join(settings.BASE_DIR, 'media', 'project_structure', 'data', file_name)
        drop_na = True   # Whether to drop rows with NaN values
        encoding = 'utf-8'  # Encoding format

        # Load the dataset using load_data
        df = load_data(file_path=file_path, drop_na=drop_na, encoding=encoding)
    except FileNotFoundError:
        df = None  # Handle file not found error

    # Pass the data to the template if it's loaded
    if df is not None:
        return render(request, 'project_structure/graphs.html')  # Passing DataFrame as dictionary
    else:
        return render(request, 'project_structure/graphs.html', {'error': 'Data not available.'})