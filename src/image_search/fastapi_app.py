# main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from PIL import Image
import os
from image_search import ImageSearcher
import image_search.image_helper as ih

app = FastAPI()

# State variables
algorithm_default = "Average Hash"
threshold_default = 1
image_path_default = f"{os.getenv('HOME')}/Pictures/Media/photos/scanned/"
image_searcher = ImageSearcher(image_path_default)

@app.post("/upload-image/")
async def upload_image(
    file: UploadFile = File(...),
    algorithm: str = Form(...),
    threshold: int = Form(...)
):
    image = Image.open(file.file)
    if image:
        similar_images = image_searcher.find_similar_image(image, "", threshold)
        return JSONResponse(content={"similar_images": similar_images})
    return JSONResponse(content={"message": "No image provided"}, status_code=400)

@app.get("/set-algorithm/")
async def set_algorithm(algorithm: str):
    global image_searcher
    current_hash_type = to_hash(algorithm)
    image_searcher = ImageSearcher(image_path_default, hash_function=current_hash_type)
    return JSONResponse(content={"message": f"Algorithm set to {algorithm}"})

@app.get("/catalog/")
async def catalog():
    global image_searcher
    image_searcher = ImageSearcher(image_path_default, hash_function=to_hash(algorithm_default), catalog=True)
    return JSONResponse(content={"message": "Cataloging completed"})

def to_hash(hash_name: str) -> str:
    if hash_name == "Average Hash":
        return "average_hash"
    elif hash_name == "PHash":
        return "phash"
    return hash_name

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
