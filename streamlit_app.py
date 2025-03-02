import streamlit as st
import numpy as np
import os
from PIL import Image
import tempfile
from suggestion import get_furniture_category_suggestion
from urllib.request import urlopen

# ✅ Use `st.query_params` instead of `st.experimental_get_query_params`
query_params = st.query_params

# **API Mode Handling**
if "api" in query_params:
    st.write("API Mode Detected")

    # Check if `image_url` is provided
    image_url = query_params.get("image_url", "")

    if image_url:
        st.write(f"Processing Image from URL: {image_url}")

        try:
            # Download the image
            image = Image.open(urlopen(image_url))

            # Convert image to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                image.convert("RGB").save(temp_file.name)  
                temp_path = temp_file.name

            # Get suggestion
            suggestion = get_furniture_category_suggestion(temp_path)

            # Clean up temporary file
            os.unlink(temp_path)

            # Return API Response as JSON
            st.json({"suggestions": suggestion})

        except Exception as e:
            st.json({"error": str(e)})

    else:
        st.json({"error": "Please provide an image_url parameter."})

# **Normal Streamlit UI Mode**
else:
    st.title("Furniture Category Suggestion")
    st.write("Upload an image of furniture, and get category suggestions.")

    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=["jpg", "jpeg", "png", "bmp", "gif", "tiff", "webp"]
    )

    if uploaded_file is not None:
        try:
            # Load and display image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            # Convert image to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                image.convert("RGB").save(temp_file.name)  
                temp_path = temp_file.name

            # Process image and get suggestion
            with st.spinner("Processing... Please wait."):
                suggestion = get_furniture_category_suggestion(temp_path)

            # Display the result
            st.success("Furniture Category Suggestions:")
            st.write(suggestion)

            # Clean up
            os.unlink(temp_path)

        except Exception as e:
            st.error(f"Error: {e}")
