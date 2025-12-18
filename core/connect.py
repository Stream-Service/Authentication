from core.database import setting
 
import boto3
from botocore.client import Config
 


 
def get_s3_client():
     
    return boto3.client(
    's3',
    endpoint_url=setting.get_bucket_endpoint(),  # includes https://
    aws_access_key_id=setting.get_bucket_access_key(),
    aws_secret_access_key=setting.get_bucket_secret_key(),
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)