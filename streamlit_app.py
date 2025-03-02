import streamlit as st
import numpy as np
import os
from PIL import Image
import tempfile

# Placeholder for your model and label names
MODEL = None  
label_names = {}  # Replace with your actual label mapping

st.title("Image Labeling and Processing App")

def process_image(image):
    """Process image using the model."""
    try:
        original_im = Image.open(image)
        resized_im, seg_map = MODEL.run(original_im)
        unique_labels = np.unique(seg_map)
        detected_objects = {label: key for key, label in label_names.items() if label in unique_labels}
        
        return resized_im, seg_map, detected_objects
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return None, None, {}

uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.getvalue())
        image_path = temp_file.name
    
    resized_im, seg_map, detected_objects = process_image(image_path)
    
    if resized_im is not None:
        st.image(resized_im, caption="Resized Image", use_column_width=True)
        st.write("Detected Objects:", detected_objects)
        
        np.save("seg_map.npy", seg_map)
        resized_im.save("resized_im.png")

        st.success("Image processed successfully!")
        
        # Color overlay processing
        r = st.slider("R", 0, 255, 255)
        g = st.slider("G", 0, 255, 0)
        b = st.slider("B", 0, 255, 0)
        key = st.selectbox("Select Object to Highlight", list(detected_objects.keys()))
        
        if st.button("Apply Mask"):
            seg_map = np.load("seg_map.npy")
            resized_im = Image.open("resized_im.png")
            
            if key in label_names:
                value = label_names[key]
                
                w, h = resized_im.size
                for i in range(h):
                    for j in range(w):
                        if seg_map[i][j] == value:
                            seg_map[i][j] = 1
                        else:
                            seg_map[i][j] = 0
                
                mask_j = np.repeat(seg_map[..., None], 3, axis=2)
                mask_j[np.where((mask_j == [1, 1, 1]).any(axis=2))] = [r, g, b]
                
                output_image = np.array(resized_im) + mask_j
                output_image = Image.fromarray(output_image.astype('uint8'))
                output_image.save("output_image.png")
                
                st.image("output_image.png", caption="Processed Image with Mask", use_column_width=True)
                st.success("Mask applied successfully!")
