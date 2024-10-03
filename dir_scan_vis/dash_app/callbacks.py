from dash import Input, Output
from .app import app
import pandas as pd
from dir_scan.models import ProjectEntity
from dir_scan_vis.dash_app.plotly_helpers import create_django_project_analysis_plot

# Callback to update the graph dynamically based on user input
@app.callback(
    Output('graph', 'figure'),
    [
        Input('search-bar', 'value'),  # For filtering based on search input
        Input('dimension-dropdown', 'value')  # For dimension selection
    ]
)
def update_graph(search_value, selected_dimension):
    # Load the data from the ProjectEntity model
    meta_df = pd.DataFrame(list(ProjectEntity.objects.all().values()))

    # Apply filter based on search input
    if search_value:
        meta_df = meta_df[meta_df.apply(lambda row: row.astype(str).str.contains(search_value, case=False).any(), axis=1)]

    # Apply additional filtering based on the selected dimension
    if selected_dimension == 'dim_1':
        # Filter based on 'filename' column (assuming 'filename' is the column name)
        meta_df = meta_df[meta_df['filename'].notnull()]  # Only include rows with non-null filenames
    elif selected_dimension == 'dim_2':
        # Filter based on 'file_extension' column (assuming 'file_extension' is the column name)
        meta_df = meta_df[meta_df['file_extension'].notnull()]  # Only include rows with non-null file extensions

    # Generate the figure using the filtered DataFrame
    figure = create_django_project_analysis_plot(meta_df)

    return figure
