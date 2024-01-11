# Libraries
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps

import streamlit as st
import gdown

import ultralytics
from ultralytics import YOLO

# hide deprication warnings which directly don't affect the working of the application
import warnings
warnings.filterwarnings("ignore")


# Page layout
st.set_page_config(
    page_title="Solar Panel Detection using YOLOv8",
    page_icon = ":satellite:",
    initial_sidebar_state = 'auto'
)


with st.sidebar:
        st.title("Solar Panel Detection")
        st.subheader("Accurate detection of ...")

# Main page heading
st.write("""
         # Solar Panel Detection using YOLOv8
         """
         )

# Sidebar
st.sidebar.header("ML Model Config")

# Model Options
model_type = st.sidebar.radio(
    "Select Task", ['Detection'])

confidence = float(st.sidebar.slider("Select Model Confidence", 25, 100, 40)) / 100


# Selecting Detection Or Segmentation
if model_type == 'Detection':
    model_path = "./downloaded_models/yolov8_medium_20e.pt"
    # model_path = Path(settings.DETECTION_MODEL)


# Load Pre-trained ML Model

# # From Google Drive:
# id = "10DXgjv9c7TONGhE38oI5oHTWff8NJmJn"
# output = 'yolov8_medium_20e.pt'
# drive_file = gdown.download(id=id, output=output, quiet=False)
# drive_file


# From local machine:
try:
    model = YOLO(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)


file = st.file_uploader("Upload your Satellite Image", type=["jpg", "png"])

def import_and_predict(image_data, model, size):
    image = ImageOps.fit(image_data, size, Image.LANCZOS)
    img = np.asarray(image.convert("RGB"))
    prediction = model.predict(img, show=True, save=True, imgsz=400, conf=confidence)
    return prediction


if file is None:
    st.text("Please upload an image file")
else:
    image = Image.open(file)
    
    detect_button = st.button("Detect Solar Panels")
    
    display_image = st.image(image, use_column_width=True)
    
    if detect_button:
        # Make prediction
        predictions = import_and_predict(image, model, (400, 400))
        
        display_image.empty()
        # Extract the names of detected objects
        # boxes = predictions[0].boxes
        # names = predictions[0].names
        res_plotted = predictions[0].plot() #[:, :, ::-1]
        st.image(res_plotted, caption='Detected Image', use_column_width=True)




### Control + C => stop streamlit app
    


### try except statement:

# try:
#     model = YOLO(model_path)
# except Exception as ex:
#     st.error(f"Unable to load model. Check the specified path: {model_path}")
#     st.error(ex)