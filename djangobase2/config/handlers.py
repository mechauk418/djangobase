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


from storages.backends.s3boto3 import S3Boto3Storage

class S3LoggingHandler(logging.Handler):
    def __init__(self, bucket_name, log_file_prefix):
        logging.Handler.__init__(self)
        self.s3_client = S3Boto3Storage(bucket_name=bucket_name)
        self.log_file_prefix = log_file_prefix

    def emit(self, record):
        log_entry = self.format(record)
        # Implement your logic for rotating file names or managing versions here
        file_name = f"{self.log_file_prefix}.log"
        self.upload_log_to_s3(file_name, log_entry)

    def upload_log_to_s3(self, file_name, log_entry):
        # Append to the file if it exists, else create a new file
        try:
            # Try to read the existing log file from S3
            content = self.s3_client.open(file_name).read()
            new_content = content + '\n' + log_entry
        except:
            new_content = log_entry
        # Write back the updated content
        self.s3_client.save(file_name, new_content)