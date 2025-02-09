from PIL import Image
import os
from django.conf import settings

def compress_image(image_path, quality=85):
    """Compress an image and overwrite the original."""
    try:
        img = Image.open(image_path)
        img = img.convert("RGB")  
        img.save(image_path, quality=quality, optimize=True)
    except Exception as e:
        print(f"Error compressing {image_path}: {e}")

def compress_all_images():
    """Compress all images in the media directory."""
    for root, dirs, files in os.walk(settings.MEDIA_ROOT):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg')):
                image_path = os.path.join(root, file)
                compress_image(image_path)
                print(f"Compressed: {image_path}")
