def rate_images(url, directory="scraped_images"):


    # Download images
    download_images(url, directory)

    # Process each image in the directory
    for filename in os.listdir(directory):
        image_path = os.path.join(directory, filename)
        predicted_values = classify_image(image_path)  # Call the existing classify_image function
  

        # Print the results
        st.text(f"Image: {filename}")
        st.text(predicted_values)
        st.text("\n")