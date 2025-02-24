import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px
#from dir_scan_vis.dash_app.custom_tooltips import apply_custom_hover
#from dir_scan_vis.dash_app.color_map_generator import create_color_map

# Function to generate the plot with only the first graph (Scatter Chart)
def create_django_project_analysis_plot(meta_df):
    # Create a 3x1 and 1x1 subplot grid
    fig = make_subplots(
        rows=2, cols=3, 
        specs=[[{"colspan": 1}, {}, {}], [{"colspan": 3}, None, None]],  # Top row has 3 plots, bottom row has 1 plot stretched
        subplot_titles=("File Size Distribution", "Metadata Update", 
                        "Django Element Type", "Metadata Age"),
        horizontal_spacing=0.05,
        vertical_spacing=0.05
    )

    # Graph A: Scatter Chart
    meta_df['file_depth'] = pd.to_numeric(meta_df['file_depth'], errors='coerce')
    fig_a = px.scatter(meta_df, x='file_extension', y='file_depth', color='file_size_category', size='file_depth',
                   labels={'file_extension': 'File Extension', 'file_depth': 'File Depth'}, template='plotly_dark')
    fig_a.update_traces(showlegend=False)
    for trace in fig_a['data']:
        fig.add_trace(trace, row=1, col=1)

    # Graph B: Box Plot
    fig_b = px.box(meta_df, x='file_extension', y='file_depth', color='meta_data_age_in_days',
                   labels={'file_extension': 'File Extension', 'file_depth': 'File Depth'}, template='plotly_dark')
    fig_b.update_traces(showlegend=False)
    for trace in fig_b['data']:
        fig.add_trace(trace, row=1, col=2)

    # Graph C: Violin Plot
    fig_c = px.violin(meta_df, x='file_extension', y='file_depth', color='django_element_type',
                   labels={'file_extension': 'File Extension', 'file_depth': 'File Depth'}, template='plotly_dark')
    fig_c.update_traces(showlegend=False)
    for trace in fig_c['data']:
        fig.add_trace(trace, row=1, col=3)

    # Graph D: Scatter Plot (spans the entire width at the base)
    meta_df['modification_time'] = pd.to_datetime(meta_df['modification_time'], errors='coerce')
    meta_df['metadata_change_time'] = pd.to_datetime(meta_df['metadata_change_time'], errors='coerce')

    # Check if the conversion was successful (ensure no NaT values in the critical columns)
    if meta_df['modification_time'].isnull().all() or meta_df['metadata_change_time'].isnull().all():
        raise ValueError("One or both of the datetime columns contain no valid datetime data")
    fig_d = px.timeline(meta_df, x_start='modification_time', x_end='metadata_change_time', y='file_extension', color='file_size_category',
                       labels={'metadata_change_time': 'Metadata Change', 'access_time': 'Last Accessed'}, template='plotly_dark')
    fig_d.update_traces(showlegend=False)
    for trace in fig_d['data']:
        fig.add_trace(trace, row=2, col=1)

    # Update layout for the entire figure with black background
    fig.update_layout(
        title="Django Project Analysis",
        template='plotly_dark',
        plot_bgcolor='black',  # Plot background color
        paper_bgcolor='black',  # Entire figure background color
        font_color='white'  # Font color for text elements
    )

    return fig