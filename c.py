import cv2
import math
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pymongo import MongoClient
import time
import RPi.GPIO as GPIO
from ultralytics import YOLO

# Start webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # กำหนดความกว้างของภาพเป็น 640 พิกเซล
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # กำหนดความสูงของภาพเป็น 480 พิกเซล

# Model
model = YOLO("v3.pt")

# MongoDB connection
MONGODB_URI = "mongodb+srv://magargame:Magarthai1@cluster0.msxpgo0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGODB_URI)
db = client.whitelist
whitelist_collection = db.list_whitelist

GPIO.setmode(GPIO.BCM)
servo_pin = 17
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 200)
pwm.start(0)

def angle_to_duty_cycle(angle):
    return 2 + (angle / 18)

# Object classes
classNames = ['0', '1', 'ก', 'ข', 'ค', 'ฆ', 'ง', 'จ', 'ฉ', 'ช', 'ฌ', 'ญ', '2', 'ฎ', 'ฐ', 'ฒ', 'ณ', 'ด', 'ต', 'ถ', 'ท', 'ธ', 'น', '3', 'บ', 'ผ', 'พ', 'ฟ', 'ภ', 'ม', 'ย', 'ร', 'ล', 'ว', '4', 'ศ', 'ษ', 'ส', 'ห', 'ฬ', 'อ', 'ฮ', '5', '6', '7', '8', '9']

# Load Thai font
font_path = "Kanit-Medium.ttf"  # Change to the path where your Thai font is located
font = ImageFont.truetype(font_path, 20)

frame_count = 0
frame_interval = 10  # ปรับตามต้องการให้ทำงานทุกเฟรมที่ถ่ายมา

check_old_value = ""
global_check = False

while True:
    success, img = cap.read()
    frame_count += 1

    if frame_count % frame_interval == 0:
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

        if len(detected_classes_string) > 0:
            if check_old_value != detected_classes_string:
                data = {"license": detected_classes_string}
                result = whitelist_collection.find_one(data)
                check_old_value = detected_classes_string
                print(check_old_value)
                if result is not None:
                    print(detected_classes_string, "Is Whitelisted!!!")
                    global_check = True
                    desired_angle = 180
                    duty_cycle = angle_to_duty_cycle(desired_angle)
                    pwm.ChangeDutyCycle(duty_cycle)
                else:
                    print(detected_classes_string, "Not Whitelisted!!!")
                    global_check = True
                    desired_angle = 0
                    duty_cycle = angle_to_duty_cycle(desired_angle)
                    pwm.ChangeDutyCycle(duty_cycle)
        else :
            desired_angle = 0
            duty_cycle = angle_to_duty_cycle(desired_angle)
            pwm.ChangeDutyCycle(duty_cycle)
                
        
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
