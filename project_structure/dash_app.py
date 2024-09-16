import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly_utils import prepare_and_save_plot, plot_file_extension_distribution, create_level_count_graph
import pandas as pd

# Parameters provided from outside the function
file_name = 'project_structure.pkl'
file_path = os.path.join(settings.BASE_DIR, 'media', 'project_structure', 'data', file_name)
drop_na = True   # Whether to drop rows with NaN values
encoding = 'utf-8'  # Encoding format

# Load the dataset using load_data
df = load_data(file_path=file_path, drop_na=drop_na, encoding=encoding)

# Create your figures
level_count_fig = create_level_count_graph(
    level_counts=df.groupby('level').size().reset_index(name='count'),
    x='level',
    y='count',
    color='level',
    title='File Count by Directory Level',
    template='plotly_dark'
)

extension_count_fig = plot_file_extension_distribution(
    df,
    min_count_threshold=6,
    x='file_extension',
    y='count',
    color='file_extension',
    title='Distribution of File Extensions',
    labels={'file_extension': 'File Extension', 'count': 'Count'}
)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1("Dash App with Multiple Graphs"),

    dcc.Tabs([
        dcc.Tab(label='File Count by Directory Level', children=[
            dcc.Graph(
                id='level-count-graph',
                figure=level_count_fig
            )
        ]),

        dcc.Tab(label='Distribution of File Extensions', children=[
            dcc.Graph(
                id='extension-count-graph',
                figure=extension_count_fig
            )
        ])
    ])
])

# Define callback(s) if needed (for interactivity)
# For example:
# @app.callback(
#     Output('some-output-component', 'children'),
#     [Input('some-input-component', 'value')]
# )
# def update_output(value):
#     # Your callback logic here
#     return value

if __name__ == '__main__':
    app.run_server(debug=True)