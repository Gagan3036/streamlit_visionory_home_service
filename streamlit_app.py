import streamlit as st
import requests
import io
from PIL import Image

st.title("Image Segmentation API")

# Upload image
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    if st.button("Process Image"):
        files = {"image": uploaded_file.getvalue()}
        response = requests.post("http://127.0.0.1:8000/imagetolabel", files=files)
        
        if response.status_code == 200:
            detected_objects = response.json()["detected_objects"]
            st.write("Detected Objects:", detected_objects)
        else:
            st.error("Error processing image")

# Process Image with RGB mask
st.subheader("Apply RGB Mask to Segmented Image")
r = st.slider("Red", 0, 255, 255)
g = st.slider("Green", 0, 255, 0)
b = st.slider("Blue", 0, 255, 0)
key = st.text_input("Enter Label Key (e.g., object1)")

if st.button("Apply Mask"):
    params = {"r": r, "g": g, "b": b, "key": key}
    response = requests.get("http://127.0.0.1:8000/process_image", params=params)

    if response.status_code == 200:
        image = Image.open(io.BytesIO(response.content))
        st.image(image, caption="Processed Image", use_column_width=True)
    else:
        st.error("Error processing image mask")
