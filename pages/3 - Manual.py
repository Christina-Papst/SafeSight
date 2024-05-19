import streamlit as st
import os

c = st.container()
c.write("This program is easy to use:")
c.write("")
c.write("Step 1: paste the link of the site you want to inspect into the input field and press enter")
c.write("")
c.write("Step 2: let the program run. Please allow for potentially longer loading time")
c.write("")
c.write("The classifications of the images will appear beneath the input field. If you want more detail, please have a look in Scraped images, where you will see every scraped image. If you want to see if any images were flagged as containing pornographic depictions of children or images of sexual violence, please look in Flagged images")