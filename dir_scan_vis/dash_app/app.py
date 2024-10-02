import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash
from dir_scan.visualization_utils.plotly_helpers import create_django_project_analysis_plot
import pandas as pd
from dir_scan.models import ProjectEntity

# Initialize the Dash app using DjangoDash
app = DjangoDash('ProjectAnalysisApp', external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load the data from ProjectEntity
meta_df = pd.DataFrame(list(ProjectEntity.objects.all().values()))

# Generate the plotly figure
figure = create_django_project_analysis_plot(meta_df)

# Define the layout for Dash
app.layout = html.Div(children=[
    dcc.Graph(id='graph', figure=figure, style={'height': '100vh'})
])
