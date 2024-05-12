def classify_image(image_path):
    
    # Load the image
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

    # Check if NSFW and age is less than 20
    if predicted_class == "nsfw" and any(age_range in ["0-2", "3-9", "10-19"] for age_range in predicted_age_ranges):
    # Copy the image to the flagged folder
        shutil.copy2(image_path, directory="flagged_images")
   
    nsfw_negative_emotions = ["sad", "disgust", "angry", "fear"]  # List of negative emotions

    if predicted_class == "nsfw" and any(predicted_emotion == emotion for emotion in nsfw_negative_emotions):
    # Copy the image to the flagged folder
        shutil.copy2(image_path, flagged_folder_path)