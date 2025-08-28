import os
from PIL import Image, ImageDraw, ImageFont

INPUT_DIR = "original"
OUTPUT_DIR = "watermarked"

os.makedirs(OUTPUT_DIR, exist_ok=True)

WATERMARK_TEXT = "Your Custom Watermark"

try:
    font = ImageFont.truetype("arial.ttf", 20) 
except:
    font = ImageFont.load_default()

def add_watermark(image_path, output_path, text=WATERMARK_TEXT):
    image = Image.open(image_path).convert("RGBA")
    width, height = image.size

    big_layer = Image.new("RGBA", (width * 2, height * 2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(big_layer)

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Add spacing
    x_step = text_width + 80
    y_step = text_height + 80

    # Loop through rows
    row_index = 0
    for y in range(0, height * 2, y_step):
        # Shift even rows slightly
        x_offset = 200 if row_index % 2 else 0

        for x in range(0, width * 2, x_step):
            draw.text((x + x_offset, y), text, font=font, fill=(255, 255, 255, 100))

        row_index += 1

    rotated = big_layer.rotate(30, expand=1)
    crop_x = (rotated.width - width) // 2
    crop_y = (rotated.height - height) // 2
    rotated_cropped = rotated.crop((crop_x, crop_y, crop_x + width, crop_y + height))

    watermarked = Image.alpha_composite(image, rotated_cropped)
    watermarked.convert("RGB").save(output_path, "JPEG")

def process_images():
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            input_path = os.path.join(INPUT_DIR, filename)
            output_path = os.path.join(OUTPUT_DIR, filename)
            add_watermark(input_path, output_path)
            print(f"Watermarked: {filename}")

if __name__ == "__main__":
    process_images()
