import cv2
from torchvision import transforms
from ultralytics import YOLO
import numpy as np
model = YOLO("modd.pt")
image_path = '1.jpg'
cv_image = cv2.imread(image_path)
img_tensor = transforms.ToTensor()(cv_image)
img_tensor = img_tensor.unsqueeze(0)
results = model.predict(source=img_tensor)

names_dict = results[0].names

probs = results[0].probs.numpy()
#print(names_dict)
#print(probs)
top1_index = results[0].probs.top1

# 
top1_probability = results[0].probs.top1conf

predicted_class_name = names_dict[top1_index]

print(f"Predicted class: {predicted_class_name}, Probability: {top1_probability}")
