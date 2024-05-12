from ultralytics import YOLO
import cv2
import math
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pymongo import MongoClient
# Start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 640)

# Model
model = YOLO("v3.pt")
MONGODB_URI = "mongodb+srv://magargame:Magarthai1@cluster0.msxpgo0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGODB_URI)

db = client.whitelist

whitelist_collection = db.list_whitelist



# Object classes
classNames = ['0', '1', 'ก', 'ข', 'ค', 'ฆ', 'ง', 'จ', 'ฉ', 'ช', 'ฌ', 'ญ', '2', 'ฎ', 'ฐ', 'ฒ', 'ณ', 'ด', 'ต', 'ถ', 'ท', 'ธ', 'น', '3', 'บ', 'ผ', 'พ', 'ฟ', 'ภ', 'ม', 'ย', 'ร', 'ล', 'ว', '4', 'ศ', 'ษ', 'ส', 'ห', 'ฬ', 'อ', 'ฮ', '5', '6', '7', '8', '9']

# Load Thai font
font_path = "Kanit-Medium.ttf"  # Change to the path where your Thai font is located
font = ImageFont.truetype(font_path, 20)

import time

# กำหนดเวลาสำหรับการตรวจจับทุก 3 วินาที
detection_interval = 3

# เวลาที่เริ่มต้นการตรวจจับ
start_time = time.time()

while True:
    current_time = time.time()
    # ตรวจสอบว่าเวลาผ่านไปเพียงพอสำหรับการตรวจจับใหม่หรือไม่
    if current_time - start_time >= detection_interval:
        success, img = cap.read()
        results = model(img, stream=True)

        # Create an image from OpenCV frame
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)

        # Create a list to store detected objects
        detected_objects = []

        # Coordinates
        for r in results:
            boxes = r.boxes

            for box in boxes:
                # Bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # Confidence
                confidence = math.ceil((box.conf[0] * 100)) / 100

                # Class name
                cls = int(box.cls[0])
                class_name = classNames[cls]

                # Store detected object information
                detected_objects.append((x1, class_name))

        # Sort detected objects by x1 (from left to right)
        detected_objects.sort(key=lambda x: x[0])

        # Build a string of class names from left to right
        detected_classes_string = "".join([obj[1] for obj in detected_objects])

        # Draw rectangles and text with custom font
        for x1, class_name in detected_objects:
            cv2.rectangle(img, (x1, y1), (x1 + 60, y1 + 30), (255, 0, 255), 3)  # draw rectangle in OpenCV
            draw.text((x1, y1), f"{class_name}", font=font, fill=(255, 0, 0))

        # Convert back to OpenCV format
        img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

        # Show the image
        cv2.imshow('Webcam', img)

        if len(detected_classes_string) > 0 :
            data = {
                "license" : detected_classes_string
            }


            result = whitelist_collection.find_one(data)
            if result is not None:
                print(detected_classes_string, "Is Whitelisted!!!")
            else:
                print(detected_classes_string, "Not Whitelisted!!!")


        
        # Reset the timer
        start_time = time.time()

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
