from dash import Input, Output
from .app import app
import pandas as pd
from dir_scan.models import ProjectEntity
from dir_scan_vis.dash_app.plotly_helpers import create_django_project_analysis_plot

# Callback to update the graph dynamically based on user input
@app.callback(
    Output('graph', 'figure'),
    [
        Input('dropdown-example', 'value'),  # For filtering based on file_extension
        Input('slider-example', 'value')     # Placeholder slider for future functionality
    ]
)
def update_graph(selected_value, slider_value):
    # Load the data from the ProjectEntity model
    meta_df = pd.DataFrame(list(ProjectEntity.objects.all().values()))

    # Apply filter based on dropdown selection (file_extension filter)
    if selected_value:
        meta_df = meta_df[meta_df['file_extension'] == selected_value]

    # Generate the figure with only the first graph (Scatter Chart)
    figure = create_django_project_analysis_plot(meta_df)

    return figure