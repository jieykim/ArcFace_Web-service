import cv2
from deepface.commons import functions, distance as dst
import ArcFace
import numpy as np
import os
import boto3
from io import BytesIO

# Load model from the directory inside the Docker container
model = ArcFace.loadModel()
model.load_weights("/app/arcface_weights.h5")

target_size = (112, 112)
detector_backend = 'opencv'
metric = 'euclidean'
s3_client = boto3.client('s3')

def findThreshold(metric):
    if metric == 'cosine':
        return 0.6871912959056619
    elif metric == 'euclidean':
        return 4.1591468986978075
    elif metric == 'euclidean_l2':
        return 1.1315718048269017
    else:
        raise ValueError("Unknown metric type")

def verify(img1, img2):
    img1_array = np.array([face_img for face_img, _, _ in img1])
    img2_array = np.array([face_img for face_img, _, _ in img2])

    img1_array = np.squeeze(img1_array, axis=1)
    img2_array = np.squeeze(img2_array, axis=1)

    img1_embedding = model.predict(img1_array)[0]
    img2_embedding = model.predict(img2_array)[0]

    if metric == 'cosine':
        distance = dst.findCosineDistance(img1_embedding, img2_embedding)
    elif metric == 'euclidean':
        distance = dst.findEuclideanDistance(img1_embedding, img2_embedding)
    elif metric == 'euclidean_l2':
        distance = dst.findEuclideanDistance(dst.l2_normalize(img1_embedding), dst.l2_normalize(img2_embedding))
    else:
        raise ValueError("Unknown metric type")

    threshold = findThreshold(metric)

    if distance <= threshold:
        return True
    else:
        return False

def lambdahandler(event, context):
    # Load image from S3 bucket for bx1
    bucket_name = event['bucket_name']
    object_key = event['file_key']

    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    image_content = response['Body'].read()

    with BytesIO(image_content) as input_stream:
        bx1 = functions.extract_faces(input_stream, target_size=target_size, detector_backend=detector_backend)

    # Assume you will provide a list of S3 keys for other images for verification
    img_keys = event['verification_image_keys']
    img_list_extraction = []

    for key in img_keys:
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        img_content = response['Body'].read()

        with BytesIO(img_content) as img_stream:
            extracted_faces = functions.extract_faces(img_stream, target_size=target_size, detector_backend=detector_backend, enforce_detection=False)
            img_list_extraction.extend(extracted_faces)

    cert = False
    for i in img_list_extraction:
        if verify(bx1, i):
            cert = True
            break

    if cert:
        return {
            "message": "등록된 사람입니다",
            "is_registered": True
        }
    else:
        return {
            "message": "미등록 인원입니다",
            "is_registered": False
        }