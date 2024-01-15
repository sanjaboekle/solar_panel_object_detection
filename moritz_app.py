# Libraries
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps

import streamlit as st
# import gdown

import ultralytics
from ultralytics import YOLO

import leafmap.foliumap as leafmap

from leafmap import tms_to_geotiff
import streamlit_folium
from geopy.geocoders import Nominatim

# hide deprication warnings which directly don't affect the working of the application
# import warnings
# warnings.filterwarnings("ignore")


# Page layout
st.set_page_config(
    page_title="Solar Panel Detection using YOLOv8",
    page_icon = ":satellite:",
    initial_sidebar_state = 'auto'
)


# Main page heading
st.write("""
         # Solar Panel Detection
         """)

# Sidebar
st.sidebar.header("Model Configuration")

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


def import_and_predict(image_data, model, size):
    image = ImageOps.fit(image_data, size, Image.LANCZOS)
    img = np.asarray(image.convert("RGB"))
    prediction = model.predict(img, show=True, save=True, imgsz=400, conf=confidence)
    return prediction



tab1, tab2 = st.tabs(["Geolocation", "Image Upload"])


### Geolocator

with tab1:
    st.header("Type in your location")

    # Ask the user for the location
    location_input = st.text_input("Enter a location:")

    if location_input == "":
        location_input = "Weiskopffstraße 16, 12459 Berlin"

    geolocator = Nominatim(user_agent="solar")

    location = geolocator.geocode(location_input)

    st.write(location.latitude, location.longitude)

    map = leafmap.Map(center=[location.latitude, location.longitude], zoom=19)
    map.add_tile_layer(
        url="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        name="Satellite",
        attribution="Map Data © Google",
    )

    # Use streamlit_folium to display the map in streamlit
    streamlit_folium.folium_static(map)

    # Define the extents of the bounding box
    longitude_extent = 0.0008
    latitude_extent = 0.0005

    # Create the bounding box
    bbox = [
        location.longitude - longitude_extent,
        location.latitude - latitude_extent,
        location.longitude + longitude_extent,
        location.latitude + latitude_extent,
    ]

    # if m.user_roi_bounds() is not None:
    #     bbox = m.user_roi_bounds()
    # else:
    #     bbox = [-95.3704, 29.6762, -95.368, 29.6775]

    location_button = st.button("Use Location")
    if location_button:

        image_path = f"satellite_image_{location}.tif"
        tms_to_geotiff(output=image_path, bbox=bbox, zoom=20, source="Satellite", overwrite=True)
    
        # Display Image
        geo_image = Image.open(image_path)
        st.image(geo_image, caption="Satellite Image")

        detect_button = st.button("Detect Solar Panels")

        if detect_button:
                # Make prediction
                predictions = import_and_predict(geo_image, model, (400, 400))
                
                # # Remove image
                # display_image.empty()

                # Plot prediction image
                res_plotted = predictions[0].plot()
                st.image(res_plotted, caption='Detected Image', use_column_width=True)

                # # Print detected objects
                # boxes = predictions[0].boxes
                # object_count = len(boxes)
                # if object_count >= 1:
                #     st.markdown(f"#### Number of panels detected: {object_count}")
                # elif object_count == 0:
                #     st.markdown("#### No panels detected!")


### Image Upload
    
with tab2:
    st.header("Upload your Satellite Image")
    file = st.file_uploader("", type=["jpg", "png"])

    if file is None:
        st.text("Please upload an image file")
    else:
        image = Image.open(file)
        
        detect_button = st.button("Detect Solar Panels")
        
        display_image = st.image(image, use_column_width=True)
        
        if detect_button:
            # Make prediction
            predictions = import_and_predict(image, model, (400, 400))
            
            # Remove image
            display_image.empty()

            # Plot prediction image
            res_plotted = predictions[0].plot()
            st.image(res_plotted, caption='Detected Image', use_column_width=True)

            # Print detected objects
            boxes = predictions[0].boxes
            object_count = len(boxes)
            if object_count >= 1:
                st.markdown(f"#### Number of panels detected: {object_count}")
            elif object_count == 0:
                st.markdown("#### No panels detected!")












### Control + C => stop streamlit app