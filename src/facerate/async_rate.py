from io import BytesIO

import httpx
from .base import BaseFaceRate
from .utils import compress_image, compress_image_bytes


class AsyncFaceRate(BaseFaceRate):
    def __init__(self):
        super().__init__()
        self.client = httpx.AsyncClient(timeout=self.timeout)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def upload_image_bytes(self, image_bytes):
        """
        Upload compressed image bytes asynchronously.

        :param image_bytes: The BytesIO object or bytes containing the compressed image data.
        :return: Parsed response from the server after the image is uploaded.
        """
        # If image_bytes is not a BytesIO instance, wrap it into BytesIO.
        if not isinstance(image_bytes, BytesIO):
            image_bytes = BytesIO(image_bytes)

        files = {'image': ('test.jpg', image_bytes.getvalue(), 'image/jpeg')}
        return await self.client.post(self.base_url, files=files)

    async def upload_image(self, image_path):
        """
        Upload an image from a given file path asynchronously.

        :param image_path: Path to the image file to be uploaded.
        :return: Parsed response from the server after the image is uploaded.
        """
        with open(image_path, 'rb') as image_file:
            image_bytes = image_file.read()
            return await self.upload_image_bytes(image_bytes)

    async def get_score_from_path(self, file_path: str, max_size_kb=100) -> dict:
        """
        Get the beauty score for a given image file by its file path.

        :param file_path: Path to the image file.
        :param max_size_kb: The maximum size of the image in kilobytes after compression.
        :return: A dictionary containing the score.
        """
        # Compress the image and get a BytesIO object
        compressed_image_bytes = compress_image(file_path, max_size_kb=max_size_kb)
        # Now get the score using the compressed image bytes
        return await self.get_score_from_bytes(compressed_image_bytes.getvalue())

    async def get_score_from_bytes(self, image_bytes) -> dict:
        """
        Get the beauty score for a given image file by its bytes.

        :param image_bytes: Bytes of the image file.
        :return: A dictionary containing the score.
        """
        # Compress the image and get a BytesIO object if it's not already one
        if not isinstance(image_bytes, BytesIO):
            image_bytes = BytesIO(image_bytes)

        compressed_image_bytes = compress_image_bytes(image_bytes)
        # Upload the image and get the score
        response = await self.upload_image_bytes(compressed_image_bytes.getvalue())
        if response.is_success:
            return self.parse_response(response.text)
        return None
