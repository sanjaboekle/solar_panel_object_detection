import streamlit as st
import os
import leafmap.foliumap as leafmap

# from samgeo import SamGeo, tms_to_geotiff, get_basemaps
from leafmap import tms_to_geotiff
import streamlit_folium
from geopy.geocoders import Nominatim


st.title("My first App")
st.write("This is my first Streamlit application.")

st.sidebar.title("My Sidebar")

# Ask the user for the location
location_input = st.text_input("Enter a location:")

if location_input == "":
    location_input = "Weiskopffstraße 16, 12459 Berlin"

geolocator = Nominatim(user_agent="solar")

location = geolocator.geocode(location_input)

st.write(location.latitude, location.longitude)

# m = leafmap.Map(center=[location.latitude, location.longitude], zoom=19)
m = leafmap.Map(center=[location.latitude, location.longitude], zoom=19)
m.add_tile_layer(
    url="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
    name="Satellite",
    attribution="Map Data © Google",
)

# Use streamlit_folium to display the map in streamlit
streamlit_folium.folium_static(m)

# Define the extents of the bounding box
longitude_extent = 0.0024
latitude_extent = 0.0013

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

image = f"satellite_image_{location}.tif"

tms_to_geotiff(output=image, bbox=bbox, zoom=20, source="Satellite", overwrite=True)

st.image(image, caption="Satellite Image")

# m2 = m.layers[-1].visible = False  # turn off the basemap
# m2.add_raster(image, layer_name="Image")
# m2
