import boto3
from botocore.client import Config

ACCESS_KEY_ID = 'xxxxxxxxxxxxxxxxxxxxxxx'
ACCESS_SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxx'
BUCKET_NAME = 'elementor-json-tables'
FILE_NAME = 'aaa.txt'


data = open(FILE_NAME, 'rb')

# S3 Connect
s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    config=Config(signature_version='s3v4')
)

# Image Uploaded
s3.Bucket(BUCKET_NAME).put_object(Key=FILE_NAME, Body=data, ACL='public-read')
print ("Done")
