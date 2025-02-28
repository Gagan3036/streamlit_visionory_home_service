from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import JSONResponse, FileResponse
import numpy as np
import os
from PIL import Image
import uvicorn
from io import BytesIO
from .colloring import DeepLabModel, label_names, download_and_load_model

app = FastAPI()

# Define paths
UPLOAD_FOLDER = "uploaded_images"
NUMPY_FOLDER = r'uploaded_images\numpy_files'
RESIZED_FOLDER = r'uploaded_images\resized_images'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(NUMPY_FOLDER, exist_ok=True)
os.makedirs(RESIZED_FOLDER, exist_ok=True)

MODEL = download_and_load_model()

@app.post("/imagetolabel")
async def imagetolabel(image: UploadFile = File(...)):
    try:
        # Save uploaded image
        image_path = os.path.join(UPLOAD_FOLDER, image.filename)
        with open(image_path, "wb") as f:
            f.write(await image.read())

        # Process image
        original_im = Image.open(image_path)
        resized_im, seg_map = MODEL.run(original_im)

        # Get unique labels
        unique_labels = np.unique(seg_map)
        detected_objects = {label: key for key, label in label_names.items() if label in unique_labels}

        # Save segmented data
        seg_map_path = os.path.join(NUMPY_FOLDER, "seg_map.npy")
        np.save(seg_map_path, seg_map)

        resized_im_path = os.path.join(RESIZED_FOLDER, "resized_im.png")
        resized_im.save(resized_im_path)

        os.remove(image_path)  # Clean up uploaded image

        return JSONResponse({"detected_objects": detected_objects})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/process_image")
async def process_image(
    r: int = Query(...),
    g: int = Query(...),
    b: int = Query(...),
    key: str = Query(...)
):
    try:
        seg_map_path = os.path.join(NUMPY_FOLDER, "seg_map.npy")
        resized_im_path = os.path.join(RESIZED_FOLDER, "resized_im.png")

        if not os.path.exists(seg_map_path) or not os.path.exists(resized_im_path):
            return JSONResponse({"error": "Missing segmentation data"}, status_code=400)

        if key not in label_names:
            return JSONResponse({"error": "Invalid key provided"}, status_code=400)

        value = label_names[key]

        # Load saved segmentation map
        seg_map = np.load(seg_map_path)
        resized_im = Image.open(resized_im_path)

        w, h = resized_im.size
        mask = (seg_map == value).astype(np.uint8) * 255

        # Apply mask color
        mask_colored = np.stack([mask * r, mask * g, mask * b], axis=-1)
        output_image = np.array(resized_im) + mask_colored
        output_image = Image.fromarray(np.clip(output_image, 0, 255).astype("uint8"))

        output_image_path = os.path.join(UPLOAD_FOLDER, "output_image.png")
        output_image.save(output_image_path)

        return FileResponse(output_image_path, media_type="image/png")
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)