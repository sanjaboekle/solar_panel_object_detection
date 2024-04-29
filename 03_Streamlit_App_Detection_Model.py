# Libraries
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps

import ultralytics
from ultralytics import YOLO

import streamlit as st
import streamlit_folium as st_folium

import folium
import leafmap.foliumap as leafmap
from leafmap import tms_to_geotiff
from geopy.geocoders import Nominatim



# Page layout
st.set_page_config(
    page_title="Solar Panel Detection using YOLOv8",
    page_icon = ":satellite:",
    initial_sidebar_state = 'collapsed',
    layout="wide"
)

# Main page heading
st.write("""
         # Solar Panel Detection
         """)

# Sidebar
st.sidebar.header("Model Configuration")

# Model Options
model_type = st.sidebar.radio(
    "Select Task", ['Detection', 'Segmentation'])

confidence = float(st.sidebar.slider("Select Model Confidence", 25, 100, 40)) / 100



# Load Pre-trained ML Model

# From local machine
if model_type == 'Detection':
    model_path = "downloaded_models/best.torchscript"

try:
    model = YOLO(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)



# Helper functions
def import_and_predict(image_data, model, size):
    image = ImageOps.fit(image_data, size, Image.LANCZOS)
    img = np.asarray(image.convert("RGB"))
    prediction = model.predict(img, imgsz=400, conf=confidence) #, show=True, save=True)
    return prediction



# Different features in different tabs

tab1, tab2 = st.tabs(["Geolocation", "Image Upload"])


### Geolocator

with tab1:

    st.header("Choose a location to detect solar panels")

    # Ask the user for the location
    location_input = st.text_input("Enter an address:")

    # Location to start from
    if location_input is "":
        location_input = "Weiskopffstraße 16, 12459 Berlin"

    # Get the location coordinates
    geolocator = Nominatim(user_agent="solar")
    location = geolocator.geocode(location_input) # contains latitude and longitude attributes


    col1, col2 = st.columns(2)

    with col1:

        # Or ask for a click on the map
        st.write("Or choose a location on the Map by clicking on it.")
        

        # Create the map
        map = leafmap.Map(
            center=[location.latitude, location.longitude], 
            zoom=18
        )
        map.add_tile_layer(
            url="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
            name="Satellite",
            attribution="Map Data © Google"
        )
        # Use streamlit_folium to display the map in streamlit
        st_map = st_folium.st_folium(map)


        # Coordinates for bounding box
        latitude = st_map["center"]["lat"]
        longitude = st_map["center"]["lng"]


        # Define the extents of the bounding box
        longitude_extent = 0.0005
        latitude_extent = 0.0003

        # Create the bounding box
        bbox = [
            longitude - longitude_extent,
            latitude - latitude_extent,
            longitude + longitude_extent,
            latitude + latitude_extent,
        ]

    with col2:
        
        st.markdown("#")
        st.markdown("######")


        image_path = f"satellite_image_{location}.tif"
        tms_to_geotiff(output=image_path, bbox=bbox, zoom=20, source="Satellite", overwrite=True)
    
        # Display Image
        geo_image = Image.open(image_path)

        # Make prediction
        predictions = import_and_predict(geo_image, model, (400, 400))
        
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