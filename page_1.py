import streamlit as st
import numpy as np
import tensorflow as tf
import PIL.Image
import cv2
import torch
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from random import randint
import pandas as pd
import requests
import os
import shutil
import hashlib


from transformers import AutoModel
from transformers import AutoModelForImageClassification, ViTImageProcessor
from transformers import ViTFeatureExtractor, ViTForImageClassification, AutoImageProcessor

# this model checks if the image is unsafe for work
MODEL = AutoModelForImageClassification.from_pretrained("Falconsai/nsfw_image_detection")
PROCESSOR = ViTImageProcessor.from_pretrained('Falconsai/nsfw_image_detection')

# this model gives an age range for a person on the picture
model = ViTForImageClassification.from_pretrained('nateraw/vit-age-classifier')
transforms = ViTFeatureExtractor.from_pretrained('nateraw/vit-age-classifier')


# Create a list of fake user agents
SCRAPEOPS_API_KEY = '0e81eee1-3ea8-4fcd-95fd-cbc2ef81daee'


def get_user_agent_list():
  response = requests.get('http://headers.scrapeops.io/v1/user-agents?api_key=' + SCRAPEOPS_API_KEY)
  json_response = response.json()
  return json_response.get('result', [])


def get_random_user_agent(user_agent_list):
  random_index = randint(0, len(user_agent_list) - 1)
  return user_agent_list[random_index]

## Retrieve User-Agent List From ScrapeOps
user_agent_list = get_user_agent_list()

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
    

    



def rate_images(url, directory="scraped_images"):


    # Download images
    # Download images
    download_images(url, directory)

    # Process each image in the directory
    # Process each image in the directory
    for filename in os.listdir(directory):
        image_path = os.path.join(directory, filename)
        img = PIL.Image.open(image_path)
    
        # Process the image and make predictions if the image is nsfw
        with torch.no_grad():
            inputs = PROCESSOR(images=img, return_tensors="pt")
            outputs = MODEL(**inputs)
            logits = outputs.logits
    
        # Get the predicted label
        predicted_label = logits.argmax(-1).item()
    
     # Map the predicted label to its corresponding class name
        label_map = MODEL.config.id2label
        predicted_class = label_map[predicted_label]

     # this part is classifying the age of the person on the picture
        model = ViTForImageClassification.from_pretrained('nateraw/vit-age-classifier')
        transforms = ViTFeatureExtractor.from_pretrained('nateraw/vit-age-classifier')
        inputs = transforms(img, return_tensors='pt')
        outputs = model(**inputs)

        proba = outputs.logits.softmax(1)
        preds = proba.argmax(1)

        id_to_age_range = {
            0: "0-2",
            1: "3-9",
            2: "10-19",
            3: "20-29",
            4: "30-39",
            5: "40-49",
            6: "50-59",
            7: "60-69",
            8: "more than 70"
        }

        # Convert predicted class indices to age ranges
        predicted_age_ranges = [id_to_age_range[pred.item()] for pred in preds]

        # this part identifies the most prevalent emotion
        image_processor = AutoImageProcessor.from_pretrained("dima806/facial_emotions_image_detection")
        model = ViTForImageClassification.from_pretrained("dima806/facial_emotions_image_detection")

        image = PIL.Image.open(image_path)
        image = np.array(image)
        image = image[:, :, :3]

        inputs = image_processor(image, return_tensors="pt")
        
        with torch.no_grad():
            logits = model(**inputs).logits

        predicted_emotion = logits.argmax(-1).item()

        # Ensure variables are strings before using f-strings
        filename = str(filename)  # Assuming filename is a path, convert to string
        predicted_class = str(predicted_class)
        predicted_age_ranges_str = ", ".join(predicted_age_ranges)  # Join list elements into a comma-separated string

        # Check if NSFW and age is less than 20
        if predicted_class == "nsfw" and any(age_range in ["0-2", "3-9", "10-19"] for age_range in predicted_age_ranges):
        # Copy the image to the flagged folder
            shutil.copy2(image_path, directory="flagged_images")
    
        nsfw_negative_emotions = ["sad", "disgust", "angry", "fear"]  # List of negative emotions

        if predicted_class == "nsfw" and any(predicted_emotion == emotion for emotion in nsfw_negative_emotions):
        # Copy the image to the flagged folder
            shutil.copy2(image_path, directory="flagged_images")
    
            # Print the results
        
        st.text(f"Image: {filename}")
        st.text("Safe or unsafe for work:", predicted_class)
        st.text("Predicted age ranges:", predicted_age_ranges)
        st.text("The most prevalent emotion is", model.config.id2label[predicted_emotion])
       


st.title("SafeSight")
st.text(" ")
st.text("Check if the images of a website contain child pornography or images of a sexually violent nature.")
st.text("If you find any materials of such a nature, please contact your local police or center for cybercrime immediately.")
st.text("This program uses artificial intelligence.")
st.text("While AI is a powerful tool in the fight against cybercrime, it cannot replace your own, natural intelligence.")
st.text("Always double-check the results")
st.text(" ")
url = st.text_input("Please enter the url you want to investigate:")

enter = st.button("Enter")
if enter:
  rate_images(url, directory="scraped_images")

