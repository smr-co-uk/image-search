
import os
from image_search import ImageSearcher
from imagehash import average_hash
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


test_data = "test_data.csv"


def before():
    if Path(test_data).exists():
        os.remove(test_data)


def create_image(text: str, color: (int, int, int) =(73, 109, 137)) -> Image:
    img = Image.new('RGB', (100, 30), color=color)

    fnt = ImageFont.load_default(18)
    d = ImageDraw.Draw(img)
    d.text((10, 10), text, font=fnt, fill=(255, 255, 0))
    return img


def test_index_images(mocker):
    before()
    root_dir = "test_images"
    # Mock os.listdir
    # mocker.patch("ImageSearcher.os.listdir", return_value=["image1.jpg", "image2.png"])
    image = create_image("hello world")
    hash_value = average_hash(image)
    mocker.patch("image_search.ImageSearcher.Image.open", return_value=image)
    mocker.patch("image_search.ImageSearcher.os.walk", return_value=[(root_dir, (), ("image1.jpg", "image2.png"))])

    # Create and test ImageSearcher
    searcher = ImageSearcher(root_dir)
    searcher.index_images()

    # Assert data is updated
    assert searcher.image_data == {"image1.jpg": hash_value, "image2.png": hash_value}


def test_find_similar(mocker):
    before()
    image1 = create_image("hello world")
    hash_value1 = average_hash(image1)
    image2 = create_image("hello world and some other image to make this image different")
    hash_value2 = average_hash(image2)

    # Mock image objects
    query_image_mock = mocker.MagicMock()
    mocker.patch("image_search.ImageSearcher.Image.open", return_value=query_image_mock)
    query_image_mock.__enter__.return_value = query_image_mock
    average_hash_mock = mocker.patch("image_search.ImageSearcher.ImageSearcher.apply_hash_function", return_value=hash_value1)

    # Set image data
    searcher = ImageSearcher("test_images")
    searcher.image_data = {"image1.jpg": hash_value1, "image2.png": hash_value2}

    # Test with similar image
    similar_images = searcher.find_similar("query_image.jpg")
    assert "test_images/image1.jpg" in similar_images

    # Test with no similar image
    image3 = create_image("And now for something completely different")
    hash_value3 = average_hash(image3)
    average_hash_mock = mocker.patch("image_search.ImageSearcher.ImageSearcher.apply_hash_function", return_value=hash_value3)
    similar_images = searcher.find_similar("query_image.jpg")
    assert similar_images == []
