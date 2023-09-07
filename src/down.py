import boto3

# AWS S3 클라이언트 생성
s3 = boto3.client('s3')

# S3 버킷 이름과 객체 키(파일 경로) 지정
bucket_name = 'file-upload-system-storage2'
object_key = 'WIN_20230621_13_29_02_Pro.jpg'  # 이미지 파일 이름

# S3 객체 메타데이터 가져오기
response = s3.head_object(Bucket=bucket_name, Key=object_key)
existing_metadata=response['Metadata']

# Content-Type을 이미지 형식에 맞게 설정 (예: image/jpeg)
new_content_type = 'image/jpeg'

# Content-Type 메타데이터 설정
s3.copy_object(
    CopySource={'Bucket': bucket_name, 'Key': object_key},
    Bucket=bucket_name,
    Key=object_key,
    MetadataDirective='REPLACE',
    Metadata = existing_metadata,
    ContentType=new_content_type
)

# 이미지 다운로드
s3.download_file(bucket_name, object_key, 'C:/Users/pc/Desktop/final/downloads')

print(f"Image downloaded with Content-Type: {new_content_type}")


# import boto3

# # AWS S3 클라이언트 생성
# s3 = boto3.client('s3')

# # S3 버킷 이름과 객체 키(파일 경로) 지정
# bucket_name = 'file-upload-system-storage2'
# object_key = 'WIN_20230621_13_29_02_Pro.jpg'  # 이미지 파일 이름
# local_path = '/tmp/temp_image.jpg'  # Lambda의 임시 저장소

# # 1. 객체를 로컬로 다운로드
# s3.download_file(bucket_name, object_key, local_path)

# # 2. 다운로드한 객체를 ContentType을 지정하여 다시 업로드
# s3.upload_file(local_path, bucket_name, object_key, ExtraArgs={'ContentType': "image/jpeg"})

# print("Content-Type has been updated to image/jpeg")