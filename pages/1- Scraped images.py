# Page 2: Displaying Scraped Images
import streamlit as st
import os

def display_scraped_images(directory="scraped_images"):
    st.title("Scraped Images")
    st.text("Displaying all scraped images:")

    # Get a list of image files in the directory
    image_files = os.listdir(directory)

    # Display each image along with its file name
    for filename in image_files:
        st.image(os.path.join(directory, filename), caption=filename, use_column_width=True)

# Run the Streamlit app for Page 2
if __name__ == "__main__":
    display_scraped_images()