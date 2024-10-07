# ﻿This application works in three steps:

1.) It scrapes every image from a url you provide and saves them in the file "scraped_images". Don´t forget to include the https:// 

2.) It classifies every image according to three criteria
- is it safe for work (does it contain pornography)?
-  how old is the subject?
-  what is the most prevalent emotion displayed by the subject?

3.) If the image is not safe for work (nsfw) and the subject is under 20 years old, or displays fear, anger, disgust or sadness, the image is copied into a separate file "flagged_images"


## ATTENTION
Artificial intelligence is a powerful tool in the fight against cybercrime. However, it should not be used indiscriminately. Always double-check the results. No program is immune against making mistakes, including this one.


## A WORD OF CAUTION:
This application is meant to combat the spread of child pornography and content depicting sexual violence. The images in the folder "flagged_images" might disturb the viewer. if you find evidence of child pornography or sexual violence, contact your local police or center for cyber crime immediately.
Thank you for helping to protect our children and to make the internet a safer space.


## SETUP OF THE SCRAPER
The first part of the webscraper contains a strategy to bypass automated website safeguards that would bar you from scraping. To do that, you need to create a free account in Scrapeops and get your own API key.
Copy the API key to the relevant part of the code:

#### Create a list of user agents
SCRAPEOPS_API_KEY = "xxxxxxx" (don´t leave out the quotation marks)

#### Scrape with care. 
It you scrape a site too often, you might inadvertently cause a shutdown because of too much traffic. This application is not meant to be misused for DDOS attacks, only as a control mechanism for images online


## Run the program
To start the program, open the Terminal and type the command "streamlit run Home.py"



