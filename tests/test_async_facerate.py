from pathlib import Path

import pytest
from facerate.async_rate import AsyncFaceRate
from httpx import AsyncClient


# This decorator is required to use async features with pytest
@pytest.mark.asyncio
async def test_get_score():
    # Instantiate the AsyncFaceRate class
    face_rate = AsyncFaceRate()

    # Mocking AsyncClient to avoid actual HTTP requests in tests
    with pytest.MonkeyPatch.context() as mp:
        # Mock the post method
        async def mock_post(*args, **kwargs):
            class MockResponse:
                def __init__(self):
                    self.status_code = 200
                    self.is_success = True
                    # Mock the text response that you would get from face-score.com
                    self.text = "<div class='facescore-text10'>82.5</div><div class='facescore-text12'>TOP 20%</div>"

            return MockResponse()

        # Apply the monkeypatch for httpx.AsyncClient.post to mock_post
        mp.setattr(AsyncClient, "post", mock_post)

        # Call the async get_score method
        result = await face_rate.get_score('path/to/your/test/image.jpg')

        # Parse the result as JSON
        result_json = json.loads(result)

        # Assert the values (these should match your mocked response)
        assert result_json['score'] == 82.5
        assert result_json['top'] == 20.0


# List of tuples containing the filename and the expected score range as (min, max)
test_images = [
    pytest.param("p1.jpg", (50, 60), id='p1'),
    pytest.param("u1.jpg", (30, 40), marks=pytest.mark.xfail(reason="This test is expected to fail because face requires zoom in / cropping"), id='u1'),
    pytest.param("u1-face-cropped.jpg", (30, 40), id='u1-face-cropped'),
    pytest.param("u2.jpg", (40, 50), id='u2'),
    pytest.param("u3.jpg", (30, 40), id='u3'),
]


# Ensure your pytest supports async, you may need to install pytest-asyncio
@pytest.mark.asyncio
@pytest.mark.parametrize("filename, score_range", test_images)
async def test_async_rate(filename, score_range):
    # Construct the full file path assuming the test runs from the project root
    # and there is a directory named 'tests' at the same level as 'src'.
    file_path = Path(__file__).parent / filename

    # Use the async_rate function to test the image
    # Instantiate the AsyncFaceRate class
    face_rate = AsyncFaceRate()
    data = await face_rate.get_score_from_path(str(file_path))

    # Ensure the response is successful
    assert data is not None

    # Check that the expected keys are present in the response
    assert 'score' in data and 'top' in data

    # Check that the score is within the expected range
    score = data['score']
    min_expected_score, max_expected_score = score_range
    assert min_expected_score <= score <= max_expected_score, f"Score {score} not in range {score_range}"
