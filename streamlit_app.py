import streamlit as st
import numpy as np
import os
from PIL import Image
import tempfile
from suggestion import get_furniture_category_suggestion

# Streamlit UI
st.title("Furniture Category Suggestion")
st.write("Upload an image of furniture, and get category suggestions.")

# File uploader (Accepts all common image formats)
supported_formats = ["jpg", "jpeg", "png", "bmp", "gif", "tiff", "webp"]
uploaded_file = st.file_uploader("Choose an image...", type=supported_formats)

if uploaded_file is not None:
    try:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Convert image to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            image.convert("RGB").save(temp_file.name)  # Convert all formats to RGB
            temp_path = temp_file.name

        # Process image and get suggestion
        with st.spinner("Processing... Please wait."):
            suggestion = get_furniture_category_suggestion(temp_path)

        # Show suggestions
        st.success("Furniture Category Suggestions:")
        st.write(suggestion)

        # Clean up temporary file
        os.unlink(temp_path)

    except Exception as e:
        st.error(f"Error: {e}")
