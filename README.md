# Backend — FastAPI S3 Presigned URL Service

Runs on EC2. Generates S3 presigned PUT URLs so the frontend can upload files directly to S3 without routing them through the server.

## Stack

- Python 3.11+
- FastAPI + Uvicorn
- boto3 (AWS SDK)
- IAM instance role for credentials (no hardcoded keys)

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # fill in AWS_REGION and S3_BUCKET_NAME
```

## Run

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API

### `POST /upload-url`

Request body:
```json
{ "filename": "photo.jpg", "content_type": "image/jpeg" }
```

Response:
```json
{ "url": "https://s3.amazonaws.com/...", "key": "uploads/<uuid>-photo.jpg" }
```

The frontend then does a `PUT` to `url` with the raw file bytes. The backend never receives the file.

## AWS Requirements

- EC2 IAM role with `s3:PutObject` on `arn:aws:s3:::your-bucket/uploads/*`
- S3 bucket CORS must allow `PUT` from the frontend origin (CloudFront domain)

## EC2 Security Group

Open inbound port **8000** (TCP) so the frontend can reach this server.
