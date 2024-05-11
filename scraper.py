import requests  # Required by download_images (if not using ScrapeOps)
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import csv
from random import randint
import pandas as pd
import os
from tkinter import * 
from tkinter.ttk import *

def get_user_agent_list():

  SCRAPEOPS_API_KEY = '0e81eee1-3ea8-4fcd-95fd-cbc2ef81daee'
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

        # Extract the filename from the URL
        filename = os.path.basename(image_url)

        # Save the image
        with requests.get(image_url, stream=True) as image_response:
            if image_response.status_code == 200:
                with open(os.path.join(directory, filename), 'wb') as file:
                    for chunk in image_response.iter_content(1024):
                        file.write(chunk)

