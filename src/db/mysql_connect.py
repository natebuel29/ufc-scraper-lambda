import mysql.connector
import logging
import boto3
import json


def get_mysql_connection():
    logging.info("Grabbing UfcPredictorRdsSecret secret")
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name='us-east-1'
    )
    secretMap = client.get_secret_value(
        SecretId="UfcPredictorRdsSecret-extTBzicS2ON", VersionStage="AWSCURRENT")
    rdsSecret = json.loads(secretMap.get("SecretString"))
    logging.info("Successfully grabbed AWS secret")
    host = rdsSecret.get("host")
    user = rdsSecret.get("username")
    password = rdsSecret.get("password")
    database = rdsSecret.get("dbname")
    con = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
    )

    return con
