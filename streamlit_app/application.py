# Import necessary libraries
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


# Helper function to import an image and predict using the model
def import_and_predict(image_data, model, size, confidence):
    # Resize the image to the specified size using the LANCZOS filter
    image = ImageOps.fit(image_data, size, Image.LANCZOS)
    # Convert the image to an RGB array
    img = np.asarray(image.convert("RGB"))
    # Use the model to predict the objects in the image
    prediction = model.predict(img, show=True, save=True, imgsz=400, conf=confidence)
    return prediction


# Main application page function
def application_page():
    # Create a sidebar for model configuration
    with st.sidebar:
        st.sidebar.header("Model Configuration")
        # Allow the user to select the task type and confidence level
        model_type = st.sidebar.radio("Select Task", ["Detection", "Segmentation"])
        confidence = (
            float(st.sidebar.slider("Select Model Confidence", 25, 100, 50)) / 100
        )

    # Load the appropriate model based on the selected task type
    if model_type == "Detection":
        model_path = "downloaded_models/best_yolov8m_50.torchscript"
    elif model_type == "Segmentation":
        model_path = "downloaded_models/best_yolov8m-seg_50.torchscript"

    # Try to load the model, and display an error if it fails
    try:
        model = YOLO(model_path)
    except Exception as ex:
        st.error(f"Unable to load model. Check the specified path: {model_path}")
        st.error(ex)

    # Create tabs for geolocation and image upload
    tab1, tab2 = st.tabs(["Geolocation", "Image Upload"])

    # Geolocation tab
    with tab1:
        st.header("Choose any location to detect solar panels")

        # Ask the user for the location
        location_input = st.text_input("Enter a location:")

        # Default location if none is provided
        if location_input is "":
            location_input = "Boppstrasse, Berlin"

        # Get the location coordinates using the Nominatim geocoder
        geolocator = Nominatim(user_agent="solar")
        location = geolocator.geocode(location_input)

        # Create two columns for the layout
        col1, col2 = st.columns(2)

        with col1:
            # Create a placeholder for the location information
            location_placeholder = st.empty()
            # Create the map
            map = leafmap.Map(
                center=[location.latitude, location.longitude],
                zoom=15,
            )
            map.add_tile_layer(
                url="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
                name="Satellite",
                attribution="Map Data © Google",
            )
            # Use streamlit_folium to display the map in streamlit
            st_map = st_folium.st_folium(map, width="150%", height=860)

            # Choose coordinates for bounding box
            if st_map["last_clicked"] is None:
                latitude = st_map["center"]["lat"]
                longitude = st_map["center"]["lng"]
            else:
                latitude = st_map["last_clicked"]["lat"]
                longitude = st_map["last_clicked"]["lng"]

            # Add location information of map center
            curr_lat, curr_long = st_map["center"]["lat"], st_map["center"]["lng"]
            location_info = geolocator.reverse((curr_lat, curr_long))

            location_info_sep = str.split(str(location_info), ", ")
            country = location_info_sep[-1]
            city = location_info_sep[-3]
            neighborhood = location_info_sep[-4]
            street = location_info_sep[-6]
            # Update the placeholder with the location information
            location_placeholder.markdown(
                f"##### {country} | {city} | {neighborhood} | {street}"
            )
            # st.markdown(f"##### {country} | {city} | {neighborhood} | {street}")

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
            counter_placeholder = st.empty()
            # if locate_and_detect:
            image_path = f"satellite_image_{location}.tif"
            tms_to_geotiff(
                output=image_path,
                bbox=bbox,
                zoom=20,
                source="Satellite",
                overwrite=True,
            )

            # Display Image
            geo_image = Image.open(image_path)
            # st.image(geo_image, caption="Satellite Image")

            # Make prediction
            predictions = import_and_predict(geo_image, model, (400, 400), confidence)

            # Plot prediction image
            res_plotted = predictions[0].plot()
            st.image(res_plotted, caption="Detected Image", use_column_width=True)

            # Print detected objects
            boxes = predictions[0].boxes
            object_count = len(boxes)
            if object_count >= 1:
                counter_placeholder.markdown(
                    f"##### Number of panels detected: {object_count}"
                )
            elif object_count == 0:
                counter_placeholder.markdown("##### No panels detected!")

    # Image Upload

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
                st.image(res_plotted, caption="Detected Image", use_column_width=True)

                # Print detected objects
                boxes = predictions[0].boxes
                object_count = len(boxes)
                if object_count >= 1:
                    st.markdown(f"#### Number of panels detected: {object_count}")
                elif object_count == 0:
                    st.markdown("#### No panels detected!")
