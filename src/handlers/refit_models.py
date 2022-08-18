import requests
import boto3
import logging


def handler(event, context):
    logging.getLogger().setLevel(logging.INFO)
    logging.info(
        f"Kicking off {context.function_name} with Lambda Request ID {context.aws_request_id}")

    # setup basic auth for api
    client = boto3.client('secretsmanager', region_name='us-east-1')
    secretMap = client.get_secret_value(
        SecretId="UfcEventPredictorApiSecret0-Z6TyTAY1hN5n", VersionStage="AWSCURRENT")
    api_key = secretMap.get("SecretString")

    api_url = f"https://api_user:{api_key}@event.ufcpredictor.com/api/refit-models"

    response = requests.get(api_url)

    logging.info(response)
