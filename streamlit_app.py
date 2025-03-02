import streamlit as st
import numpy as np
import os
import tempfile
from PIL import Image, UnidentifiedImageError
from suggestion import get_furniture_category_suggestion
from urllib.request import urlopen, Request

# Function to download image safely
def download_image(image_url):
    try:
        # Set a User-Agent to avoid request blocking
        req = Request(image_url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req) as response:
            image = Image.open(response)
            return image
    except Exception as e:
        return None, str(e)

# Use the new way to get query parameters
query_params = st.query_params

# Check for API request
if "api" in query_params and query_params["api"] == "true":
    st.write("API Mode Detected")

    if "image_url" in query_params:
        image_url = query_params["image_url"]
        st.write(f"Processing Image from URL: {image_url}")

        try:
            # Download the image
            image, error = download_image(image_url)
            if image is None:
                st.json({"error": f"Failed to download image: {error}"})
            else:
                # Convert image to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                    image.convert("RGB").save(temp_file.name)  
                    temp_path = temp_file.name

                # Process image and get suggestion
                suggestion = get_furniture_category_suggestion(temp_path)

                # Clean up temporary file
                os.unlink(temp_path)

                # Return JSON response
                st.json({"suggestions": suggestion})

        except UnidentifiedImageError:
            st.json({"error": "Invalid image format."})
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

        except UnidentifiedImageError:
            st.error("Invalid image format. Please upload a valid image.")
        except Exception as e:
            st.error(f"Error: {e}")
