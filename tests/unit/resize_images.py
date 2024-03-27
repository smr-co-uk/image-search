import os
import image_search
from PIL import Image


def resize_images():
    root_dir = "../photos"
    image_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if image_search.ImageSearcher.is_image(filename):
                # Construct the full path and print it relative to the root directory
                full_path = os.path.join(root_dir, dirpath, filename)
                relative_path = os.path.relpath(full_path, root_dir)
                image_files.append(relative_path)
                print(relative_path)
    for fp in image_files:
        print(f"Resizing {fp}")
        # 224x224 is the standard ML size so we'll go to double or 448x448
        with Image.open(fp) as im:
            im = im.resize((448, 448))
        #     im.save(fp + ".jpg", "JPEG")


if __name__ == '__main__':
    resize_images()