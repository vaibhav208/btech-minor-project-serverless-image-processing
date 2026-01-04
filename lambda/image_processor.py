import json
import os
import time
import urllib.parse
from io import BytesIO

import boto3
from PIL import Image

s3 = boto3.client("s3")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_EXTENSIONS = (".jpg", ".jpeg", ".png")

OUTPUT_BUCKET = os.environ["OUTPUT_BUCKET"]


def resize_image(image, width):
    aspect_ratio = image.height / image.width
    height = int(width * aspect_ratio)
    return image.resize((width, height), Image.LANCZOS)


def lambda_handler(event, context):
    start_time = time.time()

    print("RAW EVENT:", json.dumps(event, indent=2))

    record = event["Records"][0]
    input_bucket = record["s3"]["bucket"]["name"]

    # 🔑 FIX: decode S3 key correctly
    raw_key = record["s3"]["object"]["key"]
    object_key = urllib.parse.unquote_plus(raw_key)

    print(f"DECODED KEY: {object_key}")

    if not object_key.lower().endswith(ALLOWED_EXTENSIONS):
        print("Skipping unsupported file type")
        return {"statusCode": 200, "body": "Skipped non-image file"}

    # Fetch object
    response = s3.get_object(Bucket=input_bucket, Key=object_key)
    file_size = response["ContentLength"]

    if file_size > MAX_FILE_SIZE:
        raise ValueError("File size exceeds limit")

    image_data = response["Body"].read()
    image = Image.open(BytesIO(image_data))

    # 🔑 FIX: force format
    image_format = image.format or "JPEG"

    resized_image = resize_image(image, 800)
    thumbnail_image = resize_image(image, 200)

    resized_buffer = BytesIO()
    resized_image.save(resized_buffer, format=image_format)
    resized_buffer.seek(0)

    thumbnail_buffer = BytesIO()
    thumbnail_image.save(thumbnail_buffer, format=image_format)
    thumbnail_buffer.seek(0)

    print("Uploading resized image...")
    s3.put_object(
        Bucket=OUTPUT_BUCKET,
        Key=f"resized/{object_key}",
        Body=resized_buffer,
        ContentType=response.get("ContentType", "image/jpeg"),
    )

    print("Uploading thumbnail image...")
    s3.put_object(
        Bucket=OUTPUT_BUCKET,
        Key=f"thumbnail/{object_key}",
        Body=thumbnail_buffer,
        ContentType=response.get("ContentType", "image/jpeg"),
    )

    processing_time = round(time.time() - start_time, 2)

    print(
        {
            "file": object_key,
            "original_size": file_size,
            "processing_time_seconds": processing_time,
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps("Image processed successfully"),
    }
