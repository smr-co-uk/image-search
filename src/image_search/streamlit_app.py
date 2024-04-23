
import streamlit as st
from PIL import Image
from image_search import ImageSearcher
import os
import sys
import image_search.image_helper as ih
from argparse import ArgumentParser


def to_hash(hash_name: str) -> str:
    if hash_name == "Average Hash":
        return "average_hash"
    elif hash_name == "PHash":
        return "phash"
    return hash_name


def update_dir(key):
    choice = st.session_state[key]
    if os.path.isdir(os.path.join(st.session_state[key+'curr_dir'], choice)):
        st.session_state[key+'curr_dir'] = os.path.normpath(os.path.join(st.session_state[key+'curr_dir'], choice))
        files = sorted(os.listdir(st.session_state[key+'curr_dir']))
        files.insert(0, '..')
        files.insert(0, '.')
        st.session_state[key+'files'] = files

def st_file_selector(st_placeholder, path='.', label='Select a file/folder', key = 'selected'):
    # https://gist.github.com/benlansdell/44000c264d1b373c77497c0ea73f0ef2#file-filepicker-py
    if key+'curr_dir' not in st.session_state:
        base_path = '.' if path is None or path == '' else path
        base_path = base_path if os.path.isdir(base_path) else os.path.dirname(base_path)
        base_path = '.' if base_path is None or base_path == '' else base_path

        files = sorted(os.listdir(base_path))
        files.insert(0, '..')
        files.insert(0, '.')
        st.session_state[key+'files'] = files
        st.session_state[key+'curr_dir'] = base_path
    else:
        base_path = st.session_state[key+'curr_dir']

    selected_file = st_placeholder.selectbox(label=label,
                                        options=st.session_state[key+'files'],
                                        key=key,
                                        on_change = lambda: update_dir(key))
    selected_path = os.path.normpath(os.path.join(base_path, selected_file))
    st_placeholder.write(os.path.abspath(selected_path))

    return selected_path

def new_image_path():
    print(f"new_image_path {st.session_state.root_dir}")
    st.session_state.image_searcher = ImageSearcher(st.session_state.root_dir, hash_function=to_hash(st.session_state.algorithm))


def find_similar(image, algorithm, threshold):
    print(f"In find_similar threshold={st.session_state.threshold} algorithm={st.session_state.algorithm} counter={st.session_state.counter}")
    st.session_state.counter = st.session_state.counter + 1
    print(f"Similar images {algorithm} {threshold}")
    st.info(f"Similar images {algorithm} {threshold}")
    image_searcher = st.session_state.image_searcher
    similar_images = image_searcher.find_similar_image(image, "", threshold)
    if len(similar_images) > 24:
        st.info("Too many similar images found.")
    elif similar_images:
        st.header(f"Similar Images")
        col1, col2, col3 = st.columns(3)  # Adjust columns as needed
        for i, similar_image in enumerate(similar_images):
            with col1 if i % 3 == 0 else col2 if i % 3 == 1 else col3:
                st.image(similar_image, caption=f"Similar Image {i + 1}", use_column_width=True)
    else:
        st.info("No similar images found")


def algorithm_changed():
    print(f"In hash_type_changed threshold={st.session_state.threshold} algorithm={st.session_state.algorithm} counter={st.session_state.counter}")
    current_hash_type = to_hash(st.session_state.algorithm)
    image_searcher = ImageSearcher(st.session_state.root_dir, hash_function=current_hash_type)  # Replace with actual path
    st.session_state.image_searcher = image_searcher


def rotate():
    if st.session_state.image_angle <= -270:
        st.session_state.image_angle = 0
    else:
        st.session_state.image_angle = st.session_state.image_angle - 90
    print(f"In rotate angle {st.session_state.image_angle}")


def image_search_controls():
    hash_type = st.radio("Algorithm", ("Average Hash", "PHash"), key="algorithm", on_change=algorithm_changed)
    threshold = st.number_input("Similarity Threshold (1-10)", min_value=1, max_value=10, key="threshold")
    button = st.button("Rotate", on_click=rotate)


def image_search(uploaded_file):
    image = Image.open(uploaded_file)
    print(f"In image_search angle {st.session_state.image_angle}")
    if st.session_state.image_angle != 0:
        image = ih.rotate_image(image, st.session_state.image_angle)
    st.session_state.image = image
    st.image(st.session_state.image, caption="Uploaded Image", use_column_width=True)
    print(f"In image_search threshold={st.session_state.threshold} algorithm={st.session_state.algorithm} counter={st.session_state.counter}")
    find_similar(st.session_state.image, st.session_state.algorithm, st.session_state.threshold)

args = sys.argv[1:]
print(f"via sys.argv {args}")
parser = ArgumentParser(args)
parser.add_argument("-r", "--root_dir", required=False,
                    default=f"{os.getenv('HOME')}/Pictures/Media/photos/scanned",
                    help="The root directory to search for images and location of the catalog.")
args = parser.parse_args()
print(f"via parser {args.root_dir}")

# Create an instance of your ImageSearcher class
threshold_default = 1
algorithm_default = "average_hash"
image_path_default = f"{os.getenv('HOME')}/Pictures/Media/photos/scanned/"

# State variables to track initial load and user interaction
if "algorithm" not in st.session_state:
    st.session_state.algorithm = algorithm_default
if "threshold" not in st.session_state:
    st.session_state.threshold = threshold_default
if "image_angle" not in st.session_state:
    st.session_state.image_angle = 0
if "image" not in st.session_state:
    st.session_state.image = None
if "image_searcher" not in st.session_state:
    image_searcher = ImageSearcher(image_path_default)  # Replace with actual path
    st.session_state.image_searcher = image_searcher
if "counter" not in st.session_state:
    st.session_state.counter = 1
if "root_dir" not in st.session_state:
    st.session_state.root_dir = image_path_default

st.title("Image Similarity Search App")

st.session_state.root_dir = st_file_selector(st, key='tif', label='Choose a directory', path=st.session_state.root_dir)
st.write("Don't forget to update the image searcher to use the new path")
st.text_input("Root directory of images", value=st.session_state.root_dir, on_change=new_image_path)

uploaded_file = st.file_uploader("Choose an Image", type=["jpg", "jpeg", "png", "bmp", "gif", "tif", "tiff", "nef"],
                                 key="uploaded_file")
if uploaded_file is not None:
    image_search_controls()
    image_search(st.session_state.uploaded_file)

