import os
import boto3
from datetime import datetime

# AWS credentials are loaded from environment variables (provided by GitHub Actions secrets)
aws_access_key = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
aws_region = os.environ['AWS_DEFAULT_REGION']

# Update these values to match your setup!
bucket_name = "arsha-vidya-gurukulam-ui"
s3_config_key = "avgconfig.conf"  # S3 object key for current config
local_config_path = "config/avgconfig.conf"

# Backup key format in S3 (keeps timestamp for each backup)
backup_key = f"backup/avgconfig_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.conf"

session = boto3.Session(
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region,
)
s3 = session.client("s3")

# Step 1: Download and back up the existing config
try:
    s3.download_file(bucket_name, s3_config_key, "current_config_backup.conf")
    s3.upload_file("current_config_backup.conf", bucket_name, backup_key)
    print(f"Backed up existing config to s3://{bucket_name}/{backup_key}")
except Exception as e:
    print("No existing config to back up, or backup failed:", e)

# Step 2: Upload new config
try:
    s3.upload_file(local_config_path, bucket_name, s3_config_key)
    print(f"Uploaded new config from {local_config_path} to s3://{bucket_name}/{s3_config_key}")
except Exception as e:
    print("Config upload failed:", e)
    exit(1)

