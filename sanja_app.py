# Libraries
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps

import ultralytics
from ultralytics import YOLO

import streamlit as st
import streamlit_folium as st_folium
import streamlit_analytics

# import gdown

import folium
import leafmap.foliumap as leafmap
from leafmap import tms_to_geotiff
from geopy.geocoders import Nominatim
import hydralit_components as hc

from streamlit_app.components import footer_style, footer
from streamlit_app.home import home_page
from streamlit_app.application import application_page

# from streamlit_app import config
import os


# Page layout
st.set_page_config(
    page_title="Solar Panel Detection using YOLOv8",
    page_icon=":satellite:",
    initial_sidebar_state="expanded",
    # layout="wide",
)
streamlit_analytics.start_tracking()

max_width_str = f"max-width: {75}%;"

st.markdown(
    f"""
        <style>
        .appview-container .main .block-container{{{max_width_str}}}
        </style>
        """,
    unsafe_allow_html=True,
)

st.markdown(
    """
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;

                }
        </style>
        """,
    unsafe_allow_html=True,
)


# Footer

st.markdown(footer_style, unsafe_allow_html=True)

# Navbar from hydralit components library

HOME = "Home"
APPLICATION = "Solar Panel Detection"

# tabs = [HOME, APPLICATION]

# define what option labels and icons to display
option_data = [{"icon": "🏠", "label": HOME}, {"icon": "🤖", "label": APPLICATION}]

# override the theme, else it will use the Streamlit applied theme
over_theme = {
    "txc_inactive": "black",
    "menu_background": "#FFDD00",
    "txc_active": "white",
    "option_active": "#FFA500",
}
font_fmt = {"font-class": "h2", "font-size": "150%"}

# display a horizontal version of the option bar
active_tab = hc.option_bar(
    option_definition=option_data,
    title="",
    key="PrimaryOption",
    override_theme=over_theme,
    font_styling=font_fmt,
    horizontal_orientation=True,
)

if active_tab == HOME:
    home_page()
    with st.sidebar:
        st.sidebar.image("streamlit_app/solar_ai.png", width=500)
        st.title("Welcome to Solar Up!")
        st.markdown(
            "Solar Up, dedicated to renewable energy, embraces AI's potential to combat climate change by employing deep learning image detection and segmentation methodologies to optimize solar panel deployment, monitor installation progress, and identify potential faults."
        )
        views = streamlit_analytics.main.counts["total_pageviews"]
        st.sidebar.markdown(f"Total visits 👨🏼‍💻: {int(views)}")

elif active_tab == APPLICATION:
    application_page()
    # with st.sidebar:
    #     st.sidebar.header("Model Configuration")
    #     # Model Options
    #     model_type = st.sidebar.radio("Select Task", ["Detection", "Segmentation"])
    #     confidence = (
    #         float(st.sidebar.slider("Select Model Confidence", 25, 100, 40)) / 100
    #     )


for i in range(4):
    st.markdown("#")
st.markdown(footer, unsafe_allow_html=True)


streamlit_analytics.stop_tracking()

### Control + C => stop streamlit app
