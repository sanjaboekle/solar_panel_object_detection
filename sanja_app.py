import streamlit as st
import os
import leafmap.foliumap as leafmap

# from samgeo import SamGeo, tms_to_geotiff, get_basemaps
from leafmap import tms_to_geotiff
import streamlit_folium
from geopy.geocoders import Nominatim


dark_mode_button = st.button("Dark Mode")
light_mode_button = st.button("Light Mode")

if dark_mode_button:
    [theme]
    base = "dark"
elif light_mode_button:
    [theme]
    base = "light"


st.title("My first App")
st.write("This is my first Streamlit application.")

st.sidebar.title("My Sidebar")
