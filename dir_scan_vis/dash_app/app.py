import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash
import pandas as pd
from dir_scan.models import ProjectEntity
from dir_scan_vis.dash_app.plotly_helpers import create_django_project_analysis_plot


# Initialize the Dash app using DjangoDash
app = DjangoDash('ProjectAnalysisApp', external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load the data from ProjectEntity
def load_data():
    return pd.DataFrame(list(ProjectEntity.objects.all().values()))

# Generate the initial plot using the centralized function
def create_initial_plot(meta_df):
    return create_django_project_analysis_plot(meta_df)

# Define the layout for the Dash app
app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            html.H2(
                "Project Analysis Dashboard", 
                className='text-center', 
                style={'color': 'white', 'marginTop': '30px', 'marginBottom': '30px'}  # Added top and bottom margin
            ),
            width=12
        ),
        justify='center'
    ),
    dbc.Row([
        dbc.Col(
            dcc.Input(
                id='search-bar',
                type='text',
                placeholder='Search...',
                className='mb-4 form-control',
                style={'color': 'white', 'backgroundColor': 'black', 'borderColor': 'white'}
            ),
            width=5
        ),
        dbc.Col(
            dcc.Dropdown(
                id='dimension-dropdown',
                options=[
                    {'label': 'Filename', 'value': 'dim_1'},
                    {'label': 'File Extension', 'value': 'dim_2'},
                ],
                value='dim_1',  # Default value
                clearable=False,
                className='mb-4',
                style={
                    'backgroundColor': 'black',   # Background color for the dropdown
                    'borderColor': 'white'        # Border color for the dropdown
                }
            ),
            width=5
        ),

    ], justify='center'),
    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id='graph',
                config={
                    'displayModeBar': True,
                    'scrollZoom': True,
                },
                style={
                    'height': '70vh',  # Adjust height for better balance
                    'width': '100%',
                    'backgroundColor': 'black'
                }
            ),
            width=10  # Set width to 10 columns for centering
        )
    ], justify='center'),
    dbc.Row(
        dbc.Col(
            html.Div("Data Source: ProjectEntity", className='text-center mt-4 text-muted', style={'color': 'white'}),
            width=12
        ),
        justify='center'
    ),
], fluid=True, style={'backgroundColor': 'black'})  # Set container background color

# Define the callback to update the graph based on search and dimension selection
@app.callback(
    Output('graph', 'figure'),
    Input('search-bar', 'value'),
    Input('dimension-dropdown', 'value')
)
def update_graph(search_value, selected_dimension):
    # Load the data
    meta_df = load_data()

    # Filter the DataFrame based on the search value
    if search_value:
        meta_df = meta_df[meta_df.apply(lambda row: row.astype(str).str.contains(search_value, case=False).any(), axis=1)]

    # Generate the updated plot
    fig = create_initial_plot(meta_df)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
