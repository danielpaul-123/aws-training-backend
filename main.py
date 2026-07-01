from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import boto3
from botocore.config import Config
import os
from uuid import uuid4
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this in production
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)

REGION = os.environ["AWS_REGION"]
BUCKET = os.environ["S3_BUCKET_NAME"]

print("AWS_REGION:", REGION)
print("BUCKET:", BUCKET)

session = boto3.session.Session(region_name=REGION)

s3 = session.client(
    "s3",
    endpoint_url=f"https://s3.{REGION}.amazonaws.com",
    config=Config(
        signature_version="s3v4",
        s3={"addressing_style": "virtual"},
    ),
)

print("Endpoint:", s3.meta.endpoint_url)


class UploadRequest(BaseModel):
    filename: str
    content_type: str


@app.post("/upload-url")
def get_upload_url(body: UploadRequest):
    key = f"uploads/{uuid4()}-{body.filename}"

    url = s3.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": BUCKET,
            "Key": key,
            "ContentType": body.content_type,
        },
        ExpiresIn=300,
    )

    print("\nGenerated URL:")
    print(url)

    return {
        "url": url,
        "key": key,
    }