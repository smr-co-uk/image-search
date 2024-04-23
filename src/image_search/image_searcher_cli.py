
from .ImageSearcher import ImageSearcher
from argparse import ArgumentParser
import os


def main():
    """Parses command-line arguments and finds image files."""
    parser = ArgumentParser(description="Find image files in a directory tree.")
    parser.add_argument("-r", "--root_dir", required=True,
                        help="The root directory to search for images and location of the catalog.")
    parser.add_argument("-i", "--image", required=False,
                        help="The image to search for.")
    parser.add_argument("-t", "--threshold", required=False, default=1,
                        help="The image to search for.")
    parser.add_argument("-c", "--catalog", required=False,
                        action="store_true", default=False,
                        help="Build searcher catalog even if one already exists.")
    parser.add_argument("-v", "--verbose", required=False,
                        action="store_true", default=False,
                        help="Build searcher catalog verbose mode.")
    parser.add_argument("-f", "--hash_function", required=False,
                        default="average_hash",
                        help="""Image hash function, any supported by imagehash module. One of:
                                'average_hash' 
                                'phash'
                                'dhash' 
                                'phash_simple' 
                                'dhash_vertical' 
                                'colorhash' 
                                'whash' """)
    args = parser.parse_args()

    if not os.path.exists(args.root_dir):
        print(f"root: {args.root_dir} does not exist")
        exit(1)
    image_searcher = ImageSearcher(args.root_dir, hash_function=args.hash_function, catalog=args.catalog,
                                   verbose=args.verbose)

    # Index images if the CSV file is empty
    if not image_searcher.image_data:
        image_searcher.index_images(args.verbose)

    # Search for a specific image
    if args.image is not None:
        similar_images = image_searcher.find_similar(args.image, threshold=args.threshold)

        if similar_images:
            print(f"Similar images to {args.image}:")
            for image in similar_images:
                print(image)
        else:
            print("No similar images found.")
    else:
        print("No image, skipping search")


if __name__ == '__main__':
    main()
