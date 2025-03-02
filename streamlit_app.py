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

