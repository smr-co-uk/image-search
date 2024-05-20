
from PIL import Image
import imagehash
from imagehash import hex_to_hash, ImageHash
import csv
import os
from image_search.ImageSearch import ImageSearch


class ImageSearcher(ImageSearch):
    def __init__(self, image_set_dir: str, hash_function: str = "average_hash", catalog=False, verbose=False):
        self.image_set_dir = image_set_dir
        self.hash_function = hash_function
        self.verbose = verbose
        self.hasher = getattr(imagehash, hash_function)
        self.image_data = {}
        csv_file = f"{hash_function}.csv"

        if os.path.exists(image_set_dir):
            self.csv_file = os.path.join(image_set_dir, csv_file)
            if catalog is True:
                self.index_images(self.verbose)
            else:
                self.image_data = self.load_image_data()
        else:
            self.csv_file = csv_file

    @staticmethod
    def is_image(filename: str) -> bool:
        return filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tif", ".tiff"))

    def load_image_data(self):
        if not os.path.exists(self.csv_file):
            return {}

        data = {}
        with open(self.csv_file, "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                filename, hash_value, function = row
                data[filename] = hex_to_hash(hash_value)
        return data

    def update_image_data(self):
        with open(self.csv_file, "w") as csvfile:
            writer = csv.writer(csvfile)
            for filename, hash_value in self.image_data.items():
                writer.writerow([filename, hash_value, self.hash_function])

    def index_images(self, verbose: bool = False) -> None:
        for filename in self.find_images(self.image_set_dir):
            if self.is_image(filename):
                filepath = os.path.join(self.image_set_dir, filename)
                image = Image.open(filepath)
                hash_value = self.apply_hash_function(image)
                if verbose:
                    print(f"{filename}, {hash_value}, {self.hash_function}")
                self.image_data[filename] = hash_value
        self.update_image_data()

    def apply_hash_function(self, image: Image) -> ImageHash:
        return self.hasher(image)

    def find_similar(self, query_image_path: str, threshold=1):
        query_image = Image.open(query_image_path)
        return self.find_similar_image(query_image, query_image_path, threshold)

    def find_similar_image(self, query_image: Image, query_image_path: str, threshold=1) -> list[str]:
        similar_images = []
        if query_image is None:
            return similar_images
        query_hash = self.apply_hash_function(query_image)
        for filename, hash_value in self.image_data.items():
            if filename != query_image_path and abs(query_hash - hash_value) <= threshold:
                # similar_images.append(os.path.join(self.image_set_dir, filename))
                path = f"{os.path.join(self.image_set_dir, filename)}"
                similar_images.append(path)
        return similar_images

    def find_images(self, root_dir) -> list[str]:
        """
        Finds image files in a directory and its subdirectories and prints their pathnames
        relative to the root directory.

        Args:
          root_dir: The directory to search for images.

        return: list of image filenames
        """
        image_files = []
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if self.is_image(filename):
                    # Construct the full path and print it relative to the root directory
                    full_path = os.path.join(dirpath, filename)
                    relative_path = os.path.relpath(full_path, root_dir)
                    image_files.append(relative_path)
        return image_files

