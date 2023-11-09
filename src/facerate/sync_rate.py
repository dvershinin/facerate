import httpx
from .base import BaseFaceRate
from .utils import compress_image

class FaceRate(BaseFaceRate):
    def __init__(self):
        super().__init__()
        self.client = httpx.Client(timeout=self.timeout)

    def upload_image(self, image_path):
        with open(image_path, 'rb') as f:
            compressed_image = compress_image(f.read())
            files = {'image': ('', compressed_image, 'image/jpeg')}
            response = self.client.post(self.base_url, files=files)
            return self.parse_response(response.text)

    def get_score(self, image_path):
        result = self.upload_image(image_path)
        return result
