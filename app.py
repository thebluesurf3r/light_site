import streamlit as st
from pyspark.sql import SparkSession
import pandas as pd
import os
import psycopg2
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Custom CSS for hover effects, background, and outline animations
st.markdown(
    """
    <style>
    /* Black background for the entire app */
    body {
        background-color: #000000;
        color: white;
    }

    /* Styling for the title */
    h1 {
        color: #00FFFF;
        text-align: center;
        font-size: 40px;
        margin-bottom: 20px;
    }

    /* Text input hover effect */
    input[type="text"], input[type="password"], select {
        background-color: #333333;
        color: #00FFFF;
        border: 1px solid #00FFFF;
        padding: 9px;
        border-radius: 6px;
        outline: none;
        transition: 0.3s ease-in-out;
    }
    
    /* Hover effect for inputs */
    input[type="text"]:hover, input[type="password"]:hover, select:hover {
        background-color: #444444;
        border: 1px solid #FFFFFF;
    }

    /* Button hover effect */
    button {
        background-color: #00FFFF;
        color: black;
        font-size: 15px;
        padding: 9px;
        border: 1px solid #00FFFF;
        border-radius: 8px;
        transition: all 0.3s ease-in-out;
    }

    button:hover {
        background-color: #FFFFFF;
        color: #000000;
        border: 1px solid #FFFFFF;
        box-shadow: 0 0 9px 1px #00FFFF;
    }

    /* Outline running animation for headers */
    h2 {
        border: 1px solid #00FFFF;
        padding: 9px;
        text-align: center;
        animation: outline 2s infinite alternate;
    }

    @keyframes outline {
        from {
            border-color: #00FFFF;
            box-shadow: 0 0 10px 2px #00FFFF;
        }
        to {
            border-color: #FFFFFF;
            box-shadow: 0 0 15px 3px #FFFFFF;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit app layout and user inputs
st.title("PySpark to PostgreSQL Loader with Auto-Table Creation")

# User input for the JDBC driver path and other configurations
jdbc_driver_path = st.text_input("Enter PostgreSQL JDBC Driver Path", "/opt/spark/jars/postgresql-42.7.4.jar")
file_name = st.text_input("Enter the file name (e.g., data)", "")
file_path = st.text_input("Enter the Path to the File", f"/home/{os.getlogin()}/Projects/data_analysis/")
file_extension = st.selectbox("Choose the File Type", ['.csv', '.pkl', '.parquet'])

# Extracting table name from file_name
table_name_default = file_name if file_name else ''

# PostgreSQL connection details inputs
st.header("PostgreSQL Connection Details")
host = st.text_input("Host", "localhost")
dbname = st.text_input("Database Name", "analysis")
user = st.text_input("Username", "postgres")
password = st.text_input("Password", type="password")
port = st.number_input("Port", value=5432)

table_name = st.text_input("Enter the Table Name", table_name_default)

# Function to create Spark session
def create_spark_session(postgres_jar):
    logging.info("Creating Spark session.")
    return SparkSession.builder \
        .appName("PySpark JDBC Job") \
        .config("spark.jars", postgres_jar) \
        .getOrCreate()

# Function to load the file into a Spark DataFrame
def load_file_to_df(file_path, file_extension, spark):
    logging.info(f"Loading file {file_path} as {file_extension}.")
    if file_extension == '.csv':
        return spark.read.csv(file_path, header=True, inferSchema=True)
    elif file_extension == '.pkl':
        df_pandas = pd.read_pickle(file_path)
        return spark.createDataFrame(df_pandas)
    elif file_extension == '.parquet':
        return spark.read.parquet(file_path)
    else:
        raise ValueError("Unsupported file format")

# Function to check if database exists, if not create it
def ensure_database_exists(dbname, db_config):
    logging.info(f"Checking if database {dbname} exists.")
    try:
        conn = psycopg2.connect(
            dbname='postgres',  # Connect to the default database first
            user=db_config['user'],
            password=db_config['password'],
            host=db_config['host'],
            port=db_config['port']
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if the database exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{dbname}'")
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(f"CREATE DATABASE {dbname}")
            st.success(f"Database '{dbname}' created successfully.")
            logging.info(f"Database {dbname} created.")
        cursor.close()
        conn.close()

    except Exception as e:
        st.error(f"Error creating database: {str(e)}")
        logging.error(f"Error creating database: {str(e)}")

# Function to map PySpark data types to PostgreSQL types
def map_spark_to_postgres_type(spark_type):
    # Mapping of PySpark types to PostgreSQL types
    type_mapping = {
        "StringType": "VARCHAR",
        "IntegerType": "INTEGER",
        "LongType": "BIGINT",
        "DoubleType": "DOUBLE PRECISION",
        "FloatType": "REAL",
        "BooleanType": "BOOLEAN",
        "DateType": "DATE",
        "TimestampType": "TIMESTAMP"
    }
    return type_mapping.get(spark_type, "TEXT")  # Default to TEXT if type not found

# Function to check if table exists, if not create it
def ensure_table_exists(table_name, df, db_config):
    logging.info(f"Ensuring table {table_name} exists.")
    try:
        conn = psycopg2.connect(
            dbname=db_config['dbname'],
            user=db_config['user'],
            password=db_config['password'],
            host=db_config['host'],
            port=db_config['port']
        )
        cursor = conn.cursor()

        # Check if the table exists
        cursor.execute(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table_name}')")
        exists = cursor.fetchone()[0]

        if not exists:
            # Map PySpark data types to PostgreSQL types
            columns_with_types = [
                f"{field.name} {map_spark_to_postgres_type(field.dataType.simpleString())}"
                for field in df.schema.fields
            ]
            create_table_query = f"""
            CREATE TABLE {table_name} (
                {', '.join(columns_with_types)}
            )
            """
            cursor.execute(create_table_query)
            conn.commit()
            st.success(f"Table '{table_name}' created successfully.")
            logging.info(f"Table {table_name} created.")

        cursor.close()
        conn.close()

    except Exception as e:
        st.error(f"Error creating table: {str(e)}")
        logging.error(f"Error creating table: {str(e)}")

# Function to push Spark DataFrame to PostgreSQL
def push_df_to_postgresql(df, table_name, db_config):
    logging.info(f"Pushing DataFrame to PostgreSQL table {table_name}.")
    jdbc_url = f"jdbc:postgresql://{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    df.write \
        .format("jdbc") \
        .option("url", jdbc_url) \
        .option("dbtable", table_name) \
        .option("user", db_config['user']) \
        .option("password", db_config['password']) \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()
    logging.info("DataFrame pushed to PostgreSQL successfully.")

# Main workflow
if st.button("Push Data to PostgreSQL"):
    try:
        # Create Spark session
        spark = create_spark_session(jdbc_driver_path)

        # Create full file path
        if os.path.isabs(file_path):
            full_file_path = os.path.join(file_path, f"{file_name}{file_extension}")
        else:
            full_file_path = os.path.join(os.path.expanduser('~'), file_path.strip('/'), f"{file_name}{file_extension}")

        # Check if the file exists
        if not os.path.isfile(full_file_path):
            st.error(f"The file '{full_file_path}' does not exist. Please check the path and filename.")
            logging.error(f"File not found: {full_file_path}")
            st.stop()  # Stop the execution of the app to prevent further actions


        logging.info(f"File path resolved to: {full_file_path}")

        # Load the file into a Spark DataFrame
        df = load_file_to_df(full_file_path, file_extension, spark)

        # PostgreSQL connection details dictionary
        db_config = {
            'host': host,
            'dbname': dbname,
            'user': user,
            'password': password,
            'port': port
        }

        # Ensure the database exists
        ensure_database_exists(dbname, db_config)

        # Ensure the table exists
        ensure_table_exists(table_name, df, db_config)

        # Push DataFrame to PostgreSQL
        push_df_to_postgresql(df, table_name, db_config)

        st.success(f"Data has been successfully pushed to the table '{table_name}' in the PostgreSQL database.")
        logging.info("Workflow completed successfully.")

    except Exception as e:
        st.error(f"Error: {str(e)}")
        logging.error(f"Error in workflow: {str(e)}")

    finally:
        if 'spark' in locals():
            spark.stop()
            logging.info("Spark session stopped.")
