import streamlit as st
from flask import Flask, request, jsonify, send_from_directory, send_file
import numpy as np
import os
from PIL import Image
import tempfile
from suggestion import get_furniture_category_suggestion
from urllib.request import urlopen

app = Flask(__name__)

# Ensure the 'uploaded_images' directory exists
UPLOAD_FOLDER = r'uploaded_images'
NUMPY_FOLDER = r'uploaded_images\numpy_files'
RESIZED_FOLDER = r'uploaded_images\resized_images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(NUMPY_FOLDER):
    os.makedirs(NUMPY_FOLDER)
if not os.path.exists(RESIZED_FOLDER):
    os.makedirs(RESIZED_FOLDER)

@app.route('/get_suggestions', methods=['POST'])
def get_suggestions():
    try:
        # Check if an image file is included in the request
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        image = request.files['image']
        image_path = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(image_path)
        
        # Get furniture suggestions for the provided image
        suggestions = get_furniture_category_suggestion(image_path)
        
        # Remove the uploaded file after processing
        os.remove(image_path)
        
        return jsonify({"suggestions": suggestions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Use the new way to get query parameters
query_params = st.query_params

# Check for API request
if "api" in query_params and query_params["api"] == "true":
    st.write("API Mode Detected")

    # Check if an image URL is provided
    if "image_url" in query_params:
        image_url = query_params["image_url"]
        st.write(f"Processing Image from URL: {image_url}")

        try:
            # Download the image
            image = Image.open(urlopen(image_url))

            # Convert image to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                image.convert("RGB").save(temp_file.name)  
                temp_path = temp_file.name

            # Process image and get suggestion
            suggestion = get_furniture_category_suggestion(temp_path)

            # Clean up temporary file
            os.unlink(temp_path)

            # Display API response as JSON
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
