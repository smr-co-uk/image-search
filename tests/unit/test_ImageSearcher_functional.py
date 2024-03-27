import pytest
from image_search import ImageSearcher
from PIL import Image
from imagehash import average_hash
import os
from pathlib import Path

test_data = "functional_test_data.csv"


def test_index_images(mocker):
    image = Image.open("tests/photos/scanned/1985-06-vitesse/1985-06-vitesse_3.jpg")
    hash_value = average_hash(image)

    # Create and test ImageSearcher
    searcher = ImageSearcher("tests/photos/scanned/1985-06-vitesse/", catalog=True)
    searcher.index_images()

    # Assert data is updated
    assert searcher.image_data.get("1985-06-vitesse_3.jpg") == hash_value


def test_find_similar_images(mocker):
    searcher = ImageSearcher("tests/photos/scanned/1985-06-vitesse/")
    search_for_image = "tests/photos/positive/1985-06-vitesse_2_negative-positive.jpg"
    resx = searcher.find_similar(search_for_image)
    print(f"Looking for {search_for_image}")
    print(f"Found {resx}")
    assert len(resx) == 6

    search_for_image = "tests/photos/scanned/1985-06-vitesse/1985-06-vitesse_1.jpg"
    res = searcher.find_similar(search_for_image)
    print(f"Looking for {search_for_image}")
    print(f"Found {res}")
    assert 1 == len(res)


def test_index_images_recursively(mocker):
    search_for_image = "tests/photos/scanned/1985-06-vitesse/1985-06-vitesse_3.jpg"
    searcher = ImageSearcher("tests/photos", catalog=True)
    searcher.index_images()
    res = searcher.find_similar(search_for_image)
    print(f"Looking for {search_for_image}")
    print(f"Found {res}")
    assert len(res) == 2


def test_index_images_recursively_with_catalog_file(mocker):
    search_for_image = "tests/photos/scanned/1985-06-vitesse/1985-06-vitesse_3.jpg"
    searcher = ImageSearcher("tests/photos")
    res = searcher.find_similar(search_for_image)
    print(f"Looking for {search_for_image}")
    print(f"Found {res}")
    assert len(res) == 2
    search_for_image = "tests/photos/scanned/1985-06-vitesse/1985-06-vitesse_2.jpg"
    res = searcher.find_similar(search_for_image, threshold=1)
    print(f"Looking for {search_for_image}")
    print(f"Found {res}")
    assert len(res) == 7


def test_index_images_recursively_with_phash(mocker):
    search_for_image = "tests/photos/scanned/1985-06-vitesse/1985-06-vitesse_3.jpg"
    searcher = ImageSearcher("tests/photos", hash_function="phash", catalog=True)
    searcher.index_images()
    res = searcher.find_similar(search_for_image, threshold=3)
    print(f"Looking for {search_for_image}")
    print(f"Found {res}")
    assert 2 == len(res)
