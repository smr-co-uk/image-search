
import streamlit as st
import PIL.Image
from st_clickable_images import clickable_images

def rotate(image, angle):
    return image.rotate(angle)


uploaded_files = st.file_uploader(
    "Choose an image file",
    accept_multiple_files=True,
    type=['tif', 'tiff', 'png', 'jpg', 'jpeg', 'bmp', 'dng', 'nef']
)

images = []

for uploaded_file in uploaded_files:
    st.write("filename:", uploaded_file.name)
    st.image(uploaded_file)
    image = PIL.Image.open(uploaded_file)
    images.append(image)
    # if st.button(f'Rotate {uploaded_file.name}'):
    #     image = images[uploaded_file.name].rotate(90)
    #     st.image(image)


clicked = clickable_images(
        [
            "https://images.unsplash.com/photo-1565130838609-c3a86655db61?w=700",
            "https://images.unsplash.com/photo-1565372195458-9de0b320ef04?w=700",
            "https://images.unsplash.com/photo-1582550945154-66ea8fff25e1?w=700",
            "https://images.unsplash.com/photo-1591797442444-039f23ddcc14?w=700",
            "https://images.unsplash.com/photo-1518727818782-ed5341dbd476?w=700",
        ],
        titles=[f"Image #{str(i)}" for i in range(5)],
        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
        img_style={"margin": "5px", "height": "200px"},
    )


st.markdown(f"Image #{clicked} clicked" if clicked > -1 else "No image clicked")
