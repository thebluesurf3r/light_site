import streamlit as st
from pyspark.sql import SparkSession
import pandas as pd
import os

# Streamlit app layout and user inputs
st.title("PySpark to PostgreSQL Loader")

# User input for the JDBC driver path and other configurations
jdbc_driver_path = st.text_input("Enter PostgreSQL JDBC Driver Path", "/opt/spark/jars/postgresql-42.7.4.jar")
file_path = st.text_input("Enter the Path to the File", "/path/to/yourfile.csv")  # File path input
file_extension = st.selectbox("Choose the File Type", ['.csv', '.pkl', '.parquet'])  # File type input

# PostgreSQL connection details inputs
st.header("PostgreSQL Connection Details")
host = st.text_input("Host", "localhost")
dbname = st.text_input("Database Name", "analysis")
user = st.text_input("Username", "postgres")
password = st.text_input("Password", type="password")
port = st.number_input("Port", value=5432)

table_name = st.text_input("Enter the Table Name", "analysis_0930")

# Initialize SparkSession with the JDBC driver
def create_spark_session(postgres_jar):
    return SparkSession.builder \
        .appName("PySpark JDBC Job") \
        .config("spark.jars", postgres_jar) \
        .getOrCreate()

# Function to load the file into a Spark DataFrame
def load_file_to_df(file_path, file_extension, spark):
    if file_extension == '.csv':
        return spark.read.csv(file_path, header=True, inferSchema=True)
    elif file_extension == '.pkl':
        df_pandas = pd.read_pickle(file_path)
        return spark.createDataFrame(df_pandas)
    elif file_extension == '.parquet':
        return spark.read.parquet(file_path)
    else:
        raise ValueError("Unsupported file format")

# Function to push Spark DataFrame to PostgreSQL
def push_df_to_postgresql(df, table_name, db_config):
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

# Main workflow
if st.button("Push Data to PostgreSQL"):
    try:
        # Create Spark session
        spark = create_spark_session(jdbc_driver_path)

        # Load the file into a Spark DataFrame
        df = load_file_to_df(file_path, file_extension, spark)

        # PostgreSQL connection details dictionary
        db_config = {
            'host': host,
            'dbname': dbname,
            'user': user,
            'password': password,
            'port': port
        }

        # Push DataFrame to PostgreSQL
        push_df_to_postgresql(df, table_name, db_config)

        st.success(f"Data has been successfully pushed to the table '{table_name}' in the PostgreSQL database.")
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
    finally:
        if 'spark' in locals():
            spark.stop()