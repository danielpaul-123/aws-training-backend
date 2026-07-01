from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import boto3
import os
from uuid import uuid4
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# ponytail: allow * for training — restrict to CloudFront domain in prod
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)

s3 = boto3.client("s3", region_name=os.environ["AWS_REGION"])
BUCKET = os.environ["S3_BUCKET_NAME"]


class UploadRequest(BaseModel):
    filename: str
    content_type: str


@app.post("/upload-url")
def get_upload_url(body: UploadRequest):
    key = f"uploads/{uuid4()}-{body.filename}"
    url = s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": BUCKET, "Key": key, "ContentType": body.content_type},
        ExpiresIn=300,
    )
    return {"url": url, "key": key}
