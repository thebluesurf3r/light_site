import dash
from dash import html
from dash import dcc
import os
import pandas as pd
from plotly_utils import create_level_count_graph, plot_file_extension_distribution
from django.conf import settings
from .utils import (setup_logging,
                    log_imported_libraries,
                    scan_directories,
                    feature_engineer,
                    display_dataframe_html,
                    categorize_by_extension,
                    categorize_file_extensions,
                    check_file_location,
                    validate_app_structure,
                    generate_custom_hover,
                    create_color_map,
                    export_dataframe,
                    display_dataframe,
                    meta_df, display_log_df)
import plotly.graph_objects as go

# Parameters
file_name = 'project_structure.pkl'
file_path = os.path.join(settings.BASE_DIR, 'media', 'project_structure', 'data', file_name)
drop_na = False
encoding = 'utf-8'

# Load the dataset
df = load_data(file_path=file_path, drop_na=drop_na, encoding=encoding)

df = categorize_by_extension(df)

df['expected_location'] = df.apply(check_file_location, axis=1)

django_project_analysis_fig = create_django_project_analysis_plot(df)


# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout with graph IDs
app.layout = html.Div([
    html.H1("Dash App with Multiple Graphs"),

    dcc.Tabs([
        dcc.Tab(label='Project Analysis', children=[
            dcc.Graph(
                id='django_project_analysis_graph',
                figure=django_project_analysis_fig
            )
        ]),

        dcc.Tab(label='Distribution of File Extensions', children=[
            dcc.Graph(
                id='extension_graph',
                figure=extension_count_fig
            )
        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)