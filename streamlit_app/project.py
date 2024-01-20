import streamlit as st
import streamlit.components.v1 as components


def project_page():
    with st.sidebar:
        st.sidebar.image("streamlit_app/logo_no_background.png", width=250)
        st.title("Welcome to PanelVision!")
        st.markdown(
            "PanelVision, dedicated to renewable energy, embraces AI's potential to combat climate change by employing deep learning image detection and segmentation methodologies to optimize solar panel deployment and monitor installation progress."
        )
        st.write("\n")
        st.markdown(
            "PanelVision is our final project of a data science bootcamp at the <a href='https://www.wbscodingschool.com/' target='_blank'>WBS Coding School</a>.",
            unsafe_allow_html=True,
        )

    st.divider()
    st.markdown(
        "<h2 style='text-align: center; color: black;'>Object detection of solar panels on satellite imagery with deep learning models</h2>",
        unsafe_allow_html=True,
    )
    st.write("\n")
    components.iframe(
        "https://docs.google.com/presentation/d/e/2PACX-1vS-RukbyKF5_zVVpeCLgt38XH-GxreQ81aHlHVwOZfKnzyPUzAYqF57xlpF-FAHR4pDWJk7LmeBqi7l/embed?start=false&loop=true&delayms=3000",
        width=1000,
        height=565,
    )
    st.write("\n")
    st.markdown(
        "<h3 style='text-align: left;'>Overview</h3>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='text-align: justify;'>Solar Up is an application that combines the power of artificial intelligence with solar energy technology. Our mission is to support solar power installation and monitoring. We trained deep learning models to detect and segment solar panels from satellite imagery.</div>",
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown(
        "<h3 style='text-align: left;'>Data Collection</h3>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='text-align: justify;'><p style='text-indent: 2em;'>"
        "Several annotated solar panel datasets are already publicly accessible. However, to train our model on publicly available satellite images, we opted to utilize a dataset based on Google Maps satellite imagery. "
        "This dataset contains the complete records associated with the article <b>A crowdsourced dataset of aerial images of solar panels, their segmentation masks, and characteristics</b>, published by Gabriel Kasmi, Yves-Marie Saint-Drenan, David Trebosc, Raphaël Jolivet, Jonathan Leloux, Babacar Sarr & Laurent Dubus in Scientific data. The article is accessible <a href='https://www.nature.com/articles/s41597-023-01951-4' target='_blank'>here</a>.</p></div>",
        unsafe_allow_html=True,
    )
    st.image("streamlit_app/nature_article.png")
    st.markdown(
        "<blockquote style='text-align: justify;'><p style='text-indent: 2em;'>"
        "'The BDPV data contains the localization of more than 28000 installations. We used this localization to extract the panels’ thumbnails. During the first annotation campaign, we extracted 28807 thumbnails using Google Earth Engine (GEE)25 application programming interface (API). For the second campaign, we extracted 17325 thumbnails from the IGN Geoservices portal (https://geoservices.ign.fr/bdortho). Our thumbnails all have a resolution of 400 × 400 pixels. Thumbnails extracted from GEE API correspond to a ground sampling distance (GSD) of 0.1 m/pixel. The API directly generates this thumbnail by setting the zoom level to 20, the localization to the ground truth localization contained in BDPV, and the output size to be 400 × 400 pixels. For IGN images, the resolution of the thumbnails corresponds to a GSD of 0.2 m/pixel. The procedure for generating IGN thumbnails differs from Google. First, we downloaded geo-localized tiles from IGN’s Geoservices portal. These tiles have a resolution of 25000 × 25000 pixels, covering an area of 25 square kilometers. Then, we extracted the thumbnail by generating a 400 × 400 pixels raster centered around the location of the PV panel. Finally, we export this raster as a.png file. We do not publish the exact location of the panels for confidentiality reasons.'</p></blockquote>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<h3 style='text-align: left;'>Model Training</h3>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='text-align: justify;'><p style='text-indent: 2em;'>"
        "We used ultralytics Yolov8 models as backbone to finetune our models for solar panel detection and segmentation. See the <a href='https://docs.ultralytics.com/' target='_blank'>documentation</a>.</p></div>",
        unsafe_allow_html=True,
    )
