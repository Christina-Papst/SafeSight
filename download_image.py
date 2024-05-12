def download_images(url, directory="scraped_images"):
  

    headers = {'User-Agent': get_random_user_agent(user_agent_list)}  # Assuming you have this function

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    img_tags = soup.find_all('img')

    for img in img_tags:
        img_url = img['src']

        # Handle relative URLs by prepending the base URL
        if img_url.startswith('http') or img_url.startswith('https'):
            image_url = img_url
        else:
            image_url = url + img_url

        # Generate a unique filename based on the image URL
        filename = hashlib.sha256(image_url.encode('utf-8')).hexdigest()[:10] + ".jpg"

        # Save the image
        with requests.get(image_url, stream=True) as image_response:
            if image_response.status_code == 200:
                with open(os.path.join(directory, filename), 'wb') as file:
                    for chunk in image_response.iter_content(1024):
                        file.write(chunk)
    

    # show the results in all three categories
    st.text("Safe or unsafe for work:", predicted_class)
    st.text("Predicted age ranges:", predicted_age_ranges)
    st.text("The most prevalent emotion is", model.config.id2label[predicted_emotion])
