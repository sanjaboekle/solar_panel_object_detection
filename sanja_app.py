import streamlit as st
import folium
from streamlit_folium import folium_static

# Create a map
m = folium.Map(location=[0, 0], zoom_start=13)

# Add a marker at location (0, 0)
folium.Marker([0, 0]).add_to(m)

# Create a map container
map_container = st.container()

# Generate HTML code for fullscreen button
html_code = """
<button onclick="document.documentElement.requestFullscreen()">Fullscreen</button>
"""

# Embed the map container and the fullscreen button in an HTML element
html_element = st.html(html_code, unsafe_allow_html=True)

# Add the map to the HTML element
folium_static(m, element_id="map")
