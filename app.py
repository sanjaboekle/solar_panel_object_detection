import streamlit as st
import hydralit_components as hc

from streamlit_app.project import project_page
from streamlit_app.application import application_page
from streamlit_app.components import footer

st.set_page_config(
    page_title="PanelVision",
    page_icon=":satellite:",
    initial_sidebar_state="expanded",
    layout="wide",
)

# Navbar from hydralit components library

PROJECT = "Project"
APPLICATION = "Solar Panel Detection"

# define what option labels and icons to display
option_data = [
    {
        "icon": "ℹ️",
        "label": PROJECT,
    },
    {
        "icon": "🛰️",
        "label": APPLICATION,
    },
]

# override the theme, else it will use the Streamlit applied theme
override_theme = {
    "txc_inactive": "white",
    "menu_background": "#f8e71e",
    "txc_active": "black",
    "option_active": "#FFFFFF",
}

# display a horizontal version of the option bar
active_tab = hc.option_bar(
    option_definition=option_data,
    title="",
    key="PrimaryOption",
    override_theme=override_theme,
    horizontal_orientation=True,
)

if active_tab == PROJECT:
    project_page()

elif active_tab == APPLICATION:
    application_page()

# Footer

st.markdown(footer, unsafe_allow_html=True)
