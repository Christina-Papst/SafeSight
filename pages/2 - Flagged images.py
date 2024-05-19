import streamlit as st
import os

def display_flagged_images(directory="flagged_images"):
    st.title("Flagged Images")
    st.text("Displaying all flagged images:")

    # Get a list of flagged image files in the directory
    flagged_image_files = os.listdir(directory)

    # Display each flagged image along with its file name and classification
    for filename in flagged_image_files:
        st.image(os.path.join(directory, filename), caption=filename, use_column_width=True)
        # You can also display additional information about the image, such as its classification

# Run the Streamlit app for Page 3
if __name__ == "__main__":
    display_flagged_images()
