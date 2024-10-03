import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash
import pandas as pd
from dir_scan.models import ProjectEntity
from dir_scan_vis.dash_app.plotly_helpers import create_django_project_analysis_plot

# Initialize the Dash app using DjangoDash
app = DjangoDash('ProjectAnalysisApp')

# Load the data from ProjectEntity
meta_df = pd.DataFrame(list(ProjectEntity.objects.all().values()))

# Generate the initial plot using the centralized function
fig = create_django_project_analysis_plot(meta_df)

# Define the layout for the Dash app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id='graph',
                figure=fig,
                config={
                    'displayModeBar': True,
                    'scrollZoom': True,
                },
                style={
                    'height': '80vh',  # Set height
                    'width': '100%',    # Set width
                }
            ),
            width=12
        )
    ])
], fluid=True)


if __name__ == '__main__':
    app.run(debug=True)
