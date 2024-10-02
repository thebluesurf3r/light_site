import re
import os
import time
import logging
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.io as pio
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from queue import Queue
from threading import Thread
from sqlalchemy import create_engine, Table, Column, MetaData, String, DateTime
from django.conf import settings
from logging.handlers import RotatingFileHandler
from light_site.log import log_imported_libraries
from datetime import datetime

#=====================================================================================================================================================#
#== Global DataFrame to store log entries ==#

# Define your log DataFrame
log_df = pd.DataFrame(columns=['timestamp', 'level', 'message'])

class DataFrameLoggingHandler(logging.Handler):
    def __init__(self, dataframe, queue):
        super().__init__()
        self.dataframe = dataframe
        self.queue = queue

    def emit(self, record):
        try:
            timestamp = pd.Timestamp.now()
            level = record.levelname
            message = record.getMessage()
            self.queue.put((timestamp, level, message))
        except Exception:
            self.handleError(record)

def process_log_queue(dataframe, queue, push_interval=60):
    """
    Processes the log queue, adding new logs to the DataFrame and pushing to the database.
    """
    while True:
        while not queue.empty():
            timestamp, level, message = queue.get()
            dataframe.loc[len(dataframe)] = [timestamp, level, message]
        
        # Push to PostgreSQL at regular intervals
        if len(dataframe) > 0:
            push_to_database(dataframe)
            dataframe.drop(dataframe.index, inplace=True)  # Clear DataFrame after pushing

        time.sleep(push_interval)

def create_table_if_not_exists(engine):
    """
    Create the table 'website_log' in the 'light_site' database if it doesn't already exist,
    ensuring the column names are lowercase for compatibility with PostgreSQL.
    """
    metadata = MetaData()

    # Define table schema with lowercase column names
    website_log = Table(
        'website_log', metadata,
        Column('timestamp', DateTime, nullable=False),  # Lowercase column names
        Column('level', String, nullable=False),
        Column('message', String, nullable=False)
    )

    # Create the table if it does not exist
    metadata.create_all(engine)

def push_to_database(dataframe):
    """
    Pushes the log DataFrame to the PostgreSQL database, ensuring lowercase columns,
    and creates the table if it doesn't exist.
    """
    try:
        # Define your PostgreSQL connection string
        engine = create_engine('postgresql://postgres:password@localhost:5432/light_site')

        # Ensure lowercase column names in DataFrame
        dataframe.columns = [col.lower() for col in dataframe.columns]

        # Create the table 'website_log' if it doesn't exist
        create_table_if_not_exists(engine)

        # Insert DataFrame into the table 'website_log' (append mode)
        dataframe.to_sql('website_log', engine, if_exists='append', index=False)
        logging.info("Successfully pushed log data to PostgreSQL.")
    except Exception as e:
        logging.error(f"Error pushing data to PostgreSQL: {str(e)}")

def setup_logging(log_file='app_log.log', log_level=logging.INFO):
    """
    Set up logging configuration to log to a file, console, and DataFrame, and return a logger.
    """
    logging.root.handlers.clear()

    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Define handlers
    log_queue = Queue()
    handlers = [
        RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5),  # 10 MB per file
        logging.StreamHandler(),
        DataFrameLoggingHandler(log_df, log_queue)
    ]
    
    for handler in handlers:
        handler.setLevel(log_level)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)

    # Start a thread to process the log queue and push to the database
    log_thread = Thread(target=process_log_queue, args=(log_df, log_queue), daemon=True)
    log_thread.start()

    return logger

# Usage
logger = setup_logging(log_file='app_log.log', log_level=logging.INFO)
logger.info("Logging initialized and set up successfully.")

#=====================================================================================================================================================#
#== Function to Display Website Log ==#

logging.info(f"Log size: {log_df.shape}")

def display_log_df(log_df, rows=5, exclude_column=None):
    logging.info(f"Viewing the log: {display_log_df}")
    if exclude_column in meta_df.columns:
        log_df = log_df.drop(columns=exclude_column)
    return log_df.head(rows)

preview_log = display_log_df(log_df, rows=20)
preview_log

#=====================================================================================================================================================#