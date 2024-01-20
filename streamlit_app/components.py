# Define common styles for images and links
common_styles = """
<style>
    /* Apply to img elements and elements with class image1 or image2 */
    img, .image1, .image2 {  
        /* Limit maximum width to prevent overflow */
        max-width: 100%;  
        /* Add padding around the images */
        padding: 10px;  
        /* Smooth transformation effects */
        transition: transform .2s;  
    }
    
    /* Apply to elements with class headerStyle and on hover of image1 and image2 */
    .headerStyle, .image1:hover, .image2:hover {  
        /* Enlarge the element */
        transform: scale(1.5);  
        /* Smooth transition effects */
        transition: 0.2s;  
    }
    
    /* Apply to all states of a link */
    a:link, a:visited, a:active {  
        /* Set link color */
        color: blue;  
        /* Set background color */
        background-color: transparent;  
        /* Underline the link */
        text-decoration: underline;  
    }

    /* Apply when the link is being activated */
    a:active {  
        /* Change link color */
        color: red;  
    }

    /* Apply on hover of elements with class a2 */
    a2:hover {  
        /* Add a solid border */
        border-style: solid;  
    }
</style>
"""

# Define styles for the footer
footer_style = """
<style>
    /* Apply to elements with id MainMenu and footer */
    MainMenu, footer {  
        /* Hide the elements */
        visibility: hidden;  
    }
    /* Apply to pseudo-element after the footer */
    footer:after {  
        /* Make the pseudo-element visible */
        visibility: visible;  
        /* Display as a block element */
        display: block;  
        /* Position relative to its normal position */
        position: relative;  
        /* Add padding */
        padding: 5px;  
        /* Move slightly down */
        top: 2px;  
    }
</style>
"""

# Define the footer
footer = """
<style>
    /* Apply to elements with class footer */
    .footer {  
        /* Position relative to its normal position */
        position: relative;  
        /* Take the full width */
        width: 100%;  
        /* Align to the left */
        left: 0;  
        /* Align to the bottom */
        bottom: 0;  
        /* Set background color */
        background-color: transparent;  
        /* Push the footer to the bottom */
        margin-top: auto;  
        /* Set text color */
        color: black;  
        /* Add padding */
        padding: 24px;  
        /* Center the text */
        text-align: center;  
    }
</style>
<div class="footer">  <!-- Create a div with class footer -->
    <p style="font-size:  13px">Copyright (c) 2024 </p>  <!-- Add copyright text -->
    <p style="font-size: 13px">This software is distributed under an M!T licence. Please consult the LICENSE file for more details.</p>  <!-- Add license text -->
    <a href="https://github.com/sanjaboekle/solar_panel_object_detection"><img class="image2" src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="github" width="70" height="70"></a>  <!-- Add a link to GitHub with an image -->
</div>
"""

# Define primary color
color_style = """
<style>
    /* Apply to the root of the document */
    :root {  
        /* Define a CSS variable for the primary color */
        --primary-color: blue;  
    }
</style>
"""
