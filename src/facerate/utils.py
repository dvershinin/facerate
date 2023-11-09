from PIL import Image
import io
import os




def compress_image_bytes(image_bytes, max_size_kb=100, step=5, quality=85):
    """
    Compress an image to ensure its size is less than the specified max_size_kb.

    :param image_bytes: Bytes containing the image data or a BytesIO object
    :param max_size_kb: The maximum allowed size in kilobytes
    :param step: Step size for each iteration to reduce the dimensions and quality
    :param quality: Starting quality for JPEG saving (1-95)
    :return: BytesIO object with compressed image data
    """
    if not isinstance(image_bytes, io.BytesIO):
        image_bytes = io.BytesIO(image_bytes)

    img = Image.open(image_bytes)
    img_format = img.format

    if img_format not in ['JPEG', 'JPG']:
        img = img.convert('RGB')
        img_format = 'JPEG'

    # Ensure no EXIF data is saved
    if 'exif' in img.info:
        del img.info['exif']

    previous_size = None
    while True:
        img_bytes = io.BytesIO()  # Reset the BytesIO for saving
        img.save(img_bytes, format=img_format, quality=quality)
        img_bytes.seek(0)  # Go to the start to check the file size

        current_size = len(img_bytes.getvalue())  # Get the byte content's length
        if current_size <= max_size_kb * 1024:
            break  # Image size is within the required limit
        elif current_size == previous_size or quality <= step:
            raise ValueError(
                f"Cannot compress the image to be under {max_size_kb}KB without significant quality loss.")

        # Reduce quality or resize if necessary
        if quality > step:
            quality -= step
        else:
            width, height = img.size
            new_width = int(width * 0.9)
            new_height = int(height * 0.9)
            if new_width < 10 or new_height < 10:
                raise ValueError(
                    "Image has become too small to compress further.")
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        previous_size = current_size  # Update previous size to current size

    return img_bytes


def compress_image(file_path, max_size_kb=100, step=5, quality=85):
    """
    Compress an image to ensure its size is less than the specified max_size_kb.
    Uses compress_image_bytes function internally.

    :param file_path: Path to the original image file
    :param max_size_kb: The maximum allowed size in kilobytes
    :param step: Step size for each iteration to reduce the dimensions
    :param quality: Quality for JPEG saving (1-95)
    :return: BytesIO object with compressed image data
    """
    with open(file_path, 'rb') as image_file:
        image_bytes = image_file.read()
        return compress_image_bytes(image_bytes, max_size_kb, step, quality)
