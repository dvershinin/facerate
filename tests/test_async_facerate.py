from pathlib import Path

import pytest
from facerate.async_rate import AsyncFaceRate
from httpx import AsyncClient

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
