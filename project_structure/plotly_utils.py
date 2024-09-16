import plotly.express as px
import plotly.io as pio
import pandas as pd
import logging
import os

from utils import load_data, DataFrameLoggingHandler, log_df

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(DataFrameLoggingHandler(log_df))

#============#

def get_unique_filename(base_filename, counter):
    while os.path.isfile(f'{base_filename}_{counter}.html'):
        counter += 1
    return f'{base_filename}_{counter}.html'

#============#

def prepare_and_save_plot(fig, width=600, height=600, template='plotly_dark', 
                          plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                          font_family="Open Sans, sans-serif", font_size=10, font_color="white", 
                          hover_template=None,  
                          base_filename='plot', auto_open=False, counter=1, 
                          title=None, xaxis_title=None, yaxis_title=None,
                          legend_title=None, coloraxis_colorbar=None):
    """
    Prepare and save a Plotly figure with custom layout and settings.

    Parameters:
    fig (go.Figure): The Plotly figure to be updated.
    width (int): Width of the figure. Default is 600.
    height (int): Height of the figure. Default is 600.
    template (str): Plotly template for the figure. Default is 'plotly_dark'.
    plot_bgcolor (str): Background color of the plot area. Default is transparent.
    paper_bgcolor (str): Background color of the paper area. Default is transparent.
    font_family (str): Font family for the text. Default is 'Open Sans, sans-serif'.
    font_size (int): Font size for the text. Default is 10.
    font_color (str): Font color for the text. Default is 'white'.
    hover_template (str or None): Custom hover template for traces. If None, no custom hover template is applied.
    base_filename (str): Base name for the file. Default is 'plot'.
    auto_open (bool): Whether to open the file in the browser after saving. Default is False.
    counter (int): Counter for incrementing filenames. Default is 1.
    title (str): Title of the plot. Default is None.
    xaxis_title (str): Title for the x-axis. Default is None.
    yaxis_title (str): Title for the y-axis. Default is None.
    legend_title (str): Title for the legend. Default is None.
    coloraxis_colorbar (str or None): Title for the color axis colorbar. If None, no colorbar is added.
    """
    # Update layout
    fig.update_layout(
        width=width,
        height=height,
        template=template,
        plot_bgcolor=plot_bgcolor,
        paper_bgcolor=paper_bgcolor,
        font=dict(
            family=font_family,
            size=font_size,
            color=font_color
        ),
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        legend_title=legend_title,
        coloraxis_colorbar=dict(
            title=coloraxis_colorbar
        ) if coloraxis_colorbar else None,
    )
    
    # Set custom hover template if provided
    if hover_template:
        fig.update_traces(hovertemplate=hover_template)
    
    # Generate unique filename with counter
    filename = get_unique_filename(base_filename, counter)
    
    try:
        # Save the figure to an HTML file
        pio.write_html(fig, file=filename, auto_open=auto_open)
        logging.info(f"Figure saved successfully as: {filename}")
    except Exception as e:
        logging.error(f"Error saving figure: {e}")
    
    return fig

#============#

def create_level_count_graph(level_counts, x, y, color, title, template):
    """
    Create a bar graph showing file count by directory level.

    Parameters:
    level_counts (pd.DataFrame): DataFrame with 'level' and 'count' columns.
    x (str): Column name for x-axis.
    y (str): Column name for y-axis.
    color (str): Column name for color coding.
    title (str): Title of the graph.
    template (str): Plotly template for styling.

    Returns:
    go.Figure: Plotly figure object.
    """
    fig = px.bar(level_counts, x=x, y=y, color=color, title=title, template=template)
    return fig

logging.info("Creating level count graph with the following parameters:")
logging.info(f"X-axis: {x}, Y-axis: {y}, Color: {color}, Title: {title}, Template: {template}")


#============#

try:
    level_count_fig = create_level_count_graph(
        level_counts=df.groupby('level').size().reset_index(name='count'),
        x='level',
        y='count',
        color='level',
        title='File Count by Directory Level',
        template='plotly_dark'
    )
    logging.info("Level count graph created successfully.")
except Exception as e:
    logging.error(f"Error creating level count graph: {e}")

#============#

# Logging the preparation and saving process
logging.info("Preparing and saving the level count plot.")

# Preparing and saving the plot
try:
    prepare_and_save_plot(
        level_count_fig,
        width=1200,
        height=400,
        template='plotly_dark',
        title='File Count by Directory Level',
        xaxis_title='Level',
        yaxis_title='Count'
    )
    logging.info("Plot saved successfully.")
except Exception as e:
    logging.error(f"Error preparing and saving plot: {e}")

#============#

def plot_file_extension_distribution(df, min_count_threshold=6, x='file_extension', y='count', color='file_extension', 
                                      title='Distribution of File Extensions', labels=None):
    """
    Generate a bar chart for the distribution of file extensions.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    min_count_threshold (int): Minimum count threshold to categorize extensions.
    x (str): Column name for the x-axis.
    y (str): Column name for the y-axis.
    color (str): Column name for color coding.
    title (str): Title of the plot.
    labels (dict): Custom labels for the axes.

    Returns:
    plotly.graph_objects.Figure: The generated bar chart figure.
    """
    logging.info(f"Generating file extension distribution plot.")

    # Replace 'No Extension' with 'folders'
    df['file_extension'] = df['file_extension'].replace('No Extension', 'folders')
    
    # Count occurrences of each file_extension
    extension_counts = df['file_extension'].value_counts().reset_index()
    extension_counts.columns = [x, y]

    # Separate the counts into two groups: those with counts > min_count_threshold and those with counts <= min_count_threshold
    other_counts = extension_counts[extension_counts[y] <= min_count_threshold]
    main_counts = extension_counts[extension_counts[y] > min_count_threshold]

    # Aggregate lesser counts into 'Other'
    if not other_counts.empty:
        other_sum = other_counts[y].sum()
        other_row = pd.DataFrame({x: ['Other'], y: [other_sum]})
        final_counts = pd.concat([main_counts, other_row], ignore_index=True)
    else:
        final_counts = main_counts

    # Sort the final DataFrame by 'count' in descending order
    final_counts = final_counts.sort_values(by=y, ascending=False)

    # Create a bar chart
    extension_count_fig = px.bar(
        final_counts,
        x=x,
        y=y,
        color=color,
        title=title,
        labels=labels or {x: 'File Extension', y: 'Count'}
    )
    return extension_count_fig

#============# 

# Creating Extension Count plot
extension_count_fig = plot_file_extension_distribution(
    df,
    min_count_threshold=6,
    x='file_extension',
    y='count',
    color='file_extension',
    title='Distribution of File Extensions',
    labels={'file_extension': 'File Extension', 'count': 'Count'}
)

#============#

# Logging the preparation and saving process
logging.info("Preparing and saving the file extension distribution.")

# Preparing and saving the plot
try:
    prepare_and_save_plot(
        extension_count_fig,
        width=1200,
        height=400,
        template='plotly_dark',
    )
    logging.info("Plot saved successfully.")
except Exception as e:
    logging.error(f"Error preparing and saving plot: {e}")