
import base64
from PIL import Image
import io


def is_image_file(filename) -> bool:
    file_type = ['tif', 'tiff', 'png', 'jpg', 'jpeg', 'bmp', 'dng', 'nef']
    return '.' in filename and filename.rsplit('.', 1)


def resize_image_keep_aspect_ratio(image: Image, new_height=400) -> Image:
    width, height = image.size
    ratio = width / height
    new_width = int(ratio * new_height)
    ii = image.resize((new_width, new_height), Image.BICUBIC)
    return height, ii, width, new_height, new_width


def rotate_image(image: Image, angle) -> Image:
    return image.rotate(angle, expand=True)


def image_from_base64(contents: str) -> Image:
    if contents.startswith('data:image'):
        bcontents = contents.split(',')[-1]
        # Decode the base64 string
        image_data = base64.b64decode(bcontents)
        # Create a BytesIO object to wrap the decoded image data
        image_buffer = io.BytesIO(image_data)
        image = Image.open(image_buffer)
        return image
    return None
