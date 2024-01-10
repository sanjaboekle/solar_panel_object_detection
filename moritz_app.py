# Libraries
from pathlib import Path
import PIL

import streamlit as st

import ultralytics
from ultralytics import YOLO


# Page layout
st.set_page_config(
    page_title="Solar Panel Detection using YOLOv8",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.title("Object Detection using YOLOv8")

# Sidebar
st.sidebar.header("Header here")


# Load Pre-trained ML Model

model_path = "downloaded_models/yolov8_medium_20e/weights/best.pt"

try:
    model = YOLO(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)



### Control + C => stop streamlit app