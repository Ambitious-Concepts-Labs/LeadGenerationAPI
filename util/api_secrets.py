import json

import boto3
from botocore.exceptions import ClientError

import util.logger as logger

my_logger = logger.get_logger("api_secrets.py")


def get_secret():
    secret_name = "prod/outscraper"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        my_logger.info("Retrieved data from AWS secret manager")
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            my_logger.error("The requested secret " + secret_name + " was not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            my_logger.error("The request was invalid due to:" + str(e))
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            my_logger.error("The request had invalid params:" + str(e))
        elif e.response['Error']['Code'] == 'DecryptionFailure':
            my_logger.error("The requested secret can't be decrypted using the provided KMS key:" + str(e))
        elif e.response['Error']['Code'] == 'InternalServiceError':
            my_logger.error("An error occurred on service side:" + str(e))
        my_logger.error("Error retrieving data from AWS secret manager: " + str(e))
        raise e

    # Decrypts secret using the associated KMS key.
    secret = json.loads(get_secret_value_response['SecretString'])
    return secret
