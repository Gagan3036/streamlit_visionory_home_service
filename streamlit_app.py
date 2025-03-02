import streamlit as st
import numpy as np
import os
from PIL import Image
import tempfile
from suggestion import get_furniture_category_suggestion

# Check for API request
query_params = st.query_params()
if "api" in query_params:
    st.write("API Mode Detected")

    # Check if an image URL is provided (for basic API functionality)
    if "image_url" in query_params:
        image_url = query_params["image_url"][0]
        st.write(f"Processing Image from URL: {image_url}")

        # Download the image
        try:
            from urllib.request import urlopen
            image = Image.open(urlopen(image_url))

            # Convert image to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                image.convert("RGB").save(temp_file.name)  
                temp_path = temp_file.name

            # Process image and get suggestion
            suggestion = get_furniture_category_suggestion(temp_path)

            # Clean up temporary file
            os.unlink(temp_path)

            # Display API response
            st.json({"suggestions": suggestion})

        except Exception as e:
            st.json({"error": str(e)})
    else:
        st.json({"error": "Please provide an image_url parameter."})
else:
    # Normal Streamlit UI
    st.title("Furniture Category Suggestion")
    st.write("Upload an image of furniture, and get category suggestions.")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "bmp", "gif", "tiff", "webp"])

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                image.convert("RGB").save(temp_file.name)  
                temp_path = temp_file.name

            with st.spinner("Processing... Please wait."):
                suggestion = get_furniture_category_suggestion(temp_path)

            st.success("Furniture Category Suggestions:")
            st.write(suggestion)

            os.unlink(temp_path)

        except Exception as e:
            st.error(f"Error: {e}")
