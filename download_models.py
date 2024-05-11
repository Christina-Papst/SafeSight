# this downloads the models

# this model checks if the image is unsafe for work
MODEL = AutoModelForImageClassification.from_pretrained("Falconsai/nsfw_image_detection")
PROCESSOR = ViTImageProcessor.from_pretrained('Falconsai/nsfw_image_detection')

# this model gives an age range for a person on the picture
model = ViTForImageClassification.from_pretrained('nateraw/vit-age-classifier')
transforms = ViTFeatureExtractor.from_pretrained('nateraw/vit-age-classifier')