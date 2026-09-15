# Serverless Image Watermarking using AWS

This project automatically adds a watermark to an image using AWS Lambda.

## AWS Services Used
- Amazon S3
- AWS Lambda
- S3 Event Trigger

## Working
1. User uploads an image to the uploads/ folder in S3.
2. S3 automatically triggers the Lambda function.
3. Lambda downloads the image.
4. The watermark is added using Python Pillow.
5. The processed image is saved in the output/ folder.

## Watermark
The watermark contains my name and registration number.
