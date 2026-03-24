import os
from PIL import Image, ImageDraw, ImageFont
import pillow_heif

# Register HEIC/HEIF opener
pillow_heif.register_heif_opener()

INPUT_DIR = "original"
OUTPUT_DIR = "watermarked"

os.makedirs(OUTPUT_DIR, exist_ok=True)

WATERMARK_TEXT = "伊薇 Yvette"

# Load font
try:
    font = ImageFont.truetype("NotoSansTC-Regular.ttf", 36)
except:
    font = ImageFont.load_default()

def add_watermark(image_path, output_path, text=WATERMARK_TEXT):
    # Open image (supports HEIC now)
    image = Image.open(image_path).convert("RGBA")
    width, height = image.size

    # Create larger transparent layer
    big_layer = Image.new("RGBA", (width * 2, height * 2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(big_layer)

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Spacing
    x_step = text_width + 200
    y_step = text_height + 100

    # Add repeated watermark
    row_index = 0
    for y in range(0, height * 2, y_step):
        x_offset = 250 if row_index % 2 else 0
        for x in range(0, width * 2, x_step):
            draw.text((x + x_offset, y), text, font=font, fill=(255, 255, 255, 160))
        row_index += 1

    # Rotate and crop to original size
    rotated = big_layer.rotate(30, expand=1)
    crop_x = (rotated.width - width) // 2
    crop_y = (rotated.height - height) // 2
    rotated_cropped = rotated.crop((crop_x, crop_y, crop_x + width, crop_y + height))

    # Combine watermark with original
    watermarked = Image.alpha_composite(image, rotated_cropped)
    watermarked.convert("RGB").save(output_path, "JPEG")

def process_images():
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".heic")):
            input_path = os.path.join(INPUT_DIR, filename)
            output_path = os.path.join(OUTPUT_DIR, os.path.splitext(filename)[0] + ".jpg")
            add_watermark(input_path, output_path)
            print(f"Watermarked: {filename}")

if __name__ == "__main__":
    process_images()