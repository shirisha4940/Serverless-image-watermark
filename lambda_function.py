import boto3
from PIL import Image, ImageDraw, ImageFont
import urllib.parse
import os

s3 = boto3.client("s3")


def lambda_handler(event, context):

    # Get bucket name and uploaded file path
    bucket = event["Records"][0]["s3"]["bucket"]["name"]

    key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"]
    )

    # Only process images uploaded inside uploads/
    if not key.startswith("uploads/"):
        return {
            "statusCode": 200,
            "body": "Skipped - file is not inside uploads/"
        }

    filename = os.path.basename(key)

    input_file = f"/tmp/{filename}"
    output_file = f"/tmp/watermarked-{filename}"

    # Download original image
    s3.download_file(
        bucket,
        key,
        input_file
    )

    with Image.open(input_file) as image:

        image = image.convert("RGBA")

        watermark_layer = Image.new(
            "RGBA",
            image.size,
            (0, 0, 0, 0)
        )

        # Watermark text
        text = "Shirisha - 24UG00229"

        font = ImageFont.load_default()

        # Create temporary text image
        text_image = Image.new(
            "RGBA",
            (350, 50),
            (0, 0, 0, 0)
        )

        text_draw = ImageDraw.Draw(text_image)

        text_draw.text(
            (5, 5),
            text,
            font=font,
            fill=(255, 255, 255, 255)
        )

        # Make watermark larger
        text_image = text_image.resize(
            (700, 100)
        )

        draw = ImageDraw.Draw(watermark_layer)

        # Dark transparent background
        draw.rectangle(
            (20, 20, 750, 140),
            fill=(0, 0, 0, 150)
        )

        # Add watermark text
        watermark_layer.alpha_composite(
            text_image,
            (35, 35)
        )

        # Merge image + watermark
        result = Image.alpha_composite(
            image,
            watermark_layer
        ).convert("RGB")

        result.save(
            output_file,
            "JPEG",
            quality=95
        )

    # Save processed image inside output/
    output_key = "output/" + filename

    s3.upload_file(
        output_file,
        bucket,
        output_key,
        ExtraArgs={
            "ContentType": "image/jpeg"
        }
    )

    return {
        "statusCode": 200,
        "body": f"Watermarked image created: {output_key}"
    }
