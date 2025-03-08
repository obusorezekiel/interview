import os
import time
import boto3
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError

# Load environment variables from .env file
load_dotenv()

# MinIO settings
MINIO_URL = os.getenv("MINIO_URL")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")

# PostgreSQL settings
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# Connect to MinIO
s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_URL,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY
)

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=POSTGRES_HOST,
    database=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD
)
cursor = conn.cursor()


def process_csv_file(file_name):
    """Download and process CSV file from MinIO"""
    try:
        # Download file
        s3_client.download_file(BUCKET_NAME, file_name, file_name)
        print(f"Downloaded {file_name}")

        # Read CSV
        df = pd.read_csv(file_name)

        # Insert data into PostgreSQL
        for _, row in df.iterrows():
            cursor.execute(
                "INSERT INTO actuals (ts, value) VALUES (%s, %s)",
                (row["ts"], row["value"])
            )
        conn.commit()
        print(f"Inserted {len(df)} rows into PostgreSQL")

        # Delete processed file
        s3_client.delete_object(Bucket=BUCKET_NAME, Key=file_name)
        os.remove(file_name)
        print(f"Processed and deleted {file_name}")

    except NoCredentialsError:
        print("MinIO credentials not available")
    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Watch MinIO for new files
while True:
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    if "Contents" in response:
        for obj in response["Contents"]:
            process_csv_file(obj["Key"])
    time.sleep(10)
