# logs configuration
import logging.handlers
import boto3, os
from botocore.exceptions import ClientError


class S3RotatingFileHandler(logging.handlers.RotatingFileHandler):
    def __init__(self, filename, maxBytes=0, backupCount=0, encoding=None, delay=0):
        super().__init__(
            filename=filename, maxBytes=maxBytes, backupCount=backupCount, encoding=encoding, delay=delay
        )
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name='ap-northeast-2',
        )
        self.bucket_name = os.getenv("AWS_STORAGE_BUCKET_NAME")
        self.logs_prefix = 'logs'
        if not self.logs_prefix.endswith("/"):
            self.logs_prefix += "/"

    def emit(self, record):
        try:
            log_data = self.format(record)
            key = f"{self.logs_prefix}{record.name}.log"
            self.s3_client.put_object(Bucket=self.bucket_name, Key=key, Body=log_data)
        except ClientError as e:
            print(f"Error sending log to S3: {e}")

    def doRollover(self):
        super().doRollover()
        log_file_name = os.path.basename(self.baseFilename)