import httpx
from bs4 import BeautifulSoup
import json

from facerate.exceptions import UploadError


class FaceRate:
    def get_score(self, file_path: str) -> str:
        """Get the beauty score for the given image file synchronously.

        Args:
            file_path (str): The file path to the image file.

        Returns:
            str: A JSON string containing the score and top percentage.
        """

        headers = {
        }

        with open(file_path, 'rb') as f:

            # Create a multipart form
            files = {'image': ('test.jpg', f, 'image/jpeg')}

            # Send the POST request
            response = httpx.post(url, files=files)

            with httpx.Client() as client:
                response = client.post('https://face-score.com/en',
                                       headers=headers,
                                       files=files)

            if response.is_success:
                soup = BeautifulSoup(response.text, 'html.parser')
                score = soup.find(class_='facescore-text10').text.strip()
                top_percentage = soup.find(class_='facescore-text12').text.replace(
                    'TOP', '').strip().replace('%', '')

                data_dict = {
                    'score': float(score),
                    'top': float(top_percentage)
                }

                return json.dumps(data_dict)

            else:
                raise UploadError(
                    f"Upload failed with status code {response.status_code}")
