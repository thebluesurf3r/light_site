import dash
from dash import html
from dash import dcc
import os
import pandas as pd
from plotly_utils import create_level_count_graph, plot_file_extension_distribution
from django.conf import settings
from utils import (load_data,
                    DataFrameLoggingHandler,
                    categorize_by_extension,
                    check_file_location,
                    validate_app_structure,
                    generate_custom_hover,
                    create_color_map,
                    export_dataframe,
                    display_dataframe,
                    display_log_df,
                    log_df, df)
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

# Create figures
level_count_fig = create_level_count_graph(
    level_counts=df.groupby('level').size().reset_index(name='level_counts'),
    x='level',
    y='count',
    color='level',
    title='File Count by Directory Level',
    template='plotly_dark'
)

extension_count_fig = plot_file_extension_distribution(
    df,
    min_count_threshold=6,
    x='count',
    y='level',
    color='level',
    title='Distribution of File Extensions',
    labels={'count': 'File Extension', 'level': 'level'}
)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout with graph IDs
app.layout = html.Div([
    html.H1("Dash App with Multiple Graphs"),

    dcc.Tabs([
        dcc.Tab(label='File Count by Directory Level', children=[
            dcc.Graph(
                id='level_count_graph',
                figure=level_count_fig
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