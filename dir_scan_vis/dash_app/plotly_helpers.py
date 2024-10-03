import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px
#from dir_scan_vis.dash_app.custom_tooltips import apply_custom_hover
#from dir_scan_vis.dash_app.color_map_generator import create_color_map

# Function to generate the plot with only the first graph (Scatter Chart)
def create_django_project_analysis_plot(meta_df):
    # Ensure 'file_depth' is numeric
    meta_df['file_depth'] = pd.to_numeric(meta_df['file_depth'], errors='coerce')
    
    # Graph A: Scatter Chart
    fig = px.scatter(
        meta_df,
        x='file_extension',
        y='file_depth',
        color='file_size_category',
        size='file_depth',
        labels={'file_extension': 'File Extension', 'file_depth': 'File Depth'},
        template='plotly_dark'
    )
    
    # Update traces and layout
    fig.update_traces(showlegend=False)
    fig.update_layout(
        title="File Size Distribution vs File Depth",
        autosize=False,  # Disable autosizing to control dimensions
        width=1200,
        height=800,
        plot_bgcolor='black',
        paper_bgcolor='black',
        font_color='white',
        template='plotly_dark',
        dragmode='zoom'
    )
    
    return fig