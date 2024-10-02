#dir_scan/data_export/db_pusher.py

# Standard imports
import logging
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Local imports
from .csv_exporter import export_dataframe
from .models import ProjectEntity  

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#=====================================================================================================================================================#
#== Function to push dataFrame to database ==#

def push_dataframe_to_db(df, table_name, db_url):
    """
    Push a Pandas DataFrame to a PostgreSQL database table.

    Args:
    df (pd.DataFrame): The DataFrame to push.
    table_name (str): The target table name in the PostgreSQL database.
    db_url (str): The database URL connection string.

    Returns:
    bool: True if successful, False otherwise.
    """
    try:
        # Create database engine
        engine = create_engine(db_url)
        logging.info(f'Connection established to the database: {db_url}')
        
        # Push DataFrame to the table
        df.to_sql(table_name, con=engine, if_exists='append', index=False)
        logging.info(f'Successfully inserted data into table: {table_name}')

        return True

    except SQLAlchemyError as e:
        # Log the error if something goes wrong
        logging.error(f"Error inserting data into table {table_name}: {str(e)}")
        return False

    except Exception as e:
        # Catch any other exceptions
        logging.error(f"Unexpected error: {str(e)}")
        return False


db_url = "postgresql+psycopg2://postgres:password@localhost:5432/job_applications"
if push_dataframe_to_db(meta_df, 'project_structure_projectentity', db_url):
    logging.info("Data successfully pushed to the database.")
else:
    logging.info("Failed to push data to the database.")