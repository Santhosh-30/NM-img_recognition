import ibm_boto3
from ibm_botocore.exceptions import ClientError

# Initialize the IBM Cloud Object Storage client
cos_client = ibm_boto3.client(
    's3',
    aws_access_key_id='YOUR_API_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY',
    endpoint_url='https://s3.us-south.cloud-object-storage.appdomain.cloud'
)

# Define the source and destination volume IDs
source_volume_id = 'YOUR_VOLUME_ID'
destination_volume_id = 'YOUR_BACKUP_VOLUME_ID'

# Create a snapshot of the source volume
try:
    response = cos_client.create_multipart_upload(
        Bucket=destination_volume_id,
        Key=f'backup_{source_volume_id}.img'
    )
    upload_id = response['UploadId']
    parts = []

    response = cos_client.upload_part_copy(
        Bucket=destination_volume_id,
        Key=f'backup_{source_volume_id}.img',
        PartNumber=1,
        UploadId=upload_id,
        CopySource={'Bucket': source_volume_id, 'Key': 'source.img'}
    )
    parts.append({'PartNumber': 1, 'ETag': response['CopyPartResult']['ETag']})

    # Complete the multipart upload
    cos_client.complete_multipart_upload(
        Bucket=destination_volume_id,
        Key=f'backup_{source_volume_id}.img',
        MultipartUpload={'Parts': parts},
        UploadId=upload_id
    )

    print(f'Successfully created a backup of {source_volume_id}')
except ClientError as e:
    print(f'Error: {e}')
