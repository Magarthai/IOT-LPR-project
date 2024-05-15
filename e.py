import cv2
import math
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pymongo import MongoClient
import time
import RPi.GPIO as GPIO
from ultralytics import YOLO

# Font
font_path = "Kanit-Medium.ttf"
font = ImageFont.truetype(font_path, 20)

# GPIO setup
GPIO.setmode(GPIO.BCM)
servo_pin = 27
servo2_pin = 25
ir_sensor_pin = 17
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(servo2_pin, GPIO.OUT)
GPIO.setup(ir_sensor_pin, GPIO.IN)
pwm = GPIO.PWM(servo_pin, 50)
pwm2 = GPIO.PWM(servo2_pin, 50)

def angle_to_duty_cycle(angle):
    return (angle / 18) + 2

def set_angle(angle, pwm):
    duty_cycle = angle_to_duty_cycle(angle)
    pwm.start(duty_cycle)
    time.sleep(1)

# Start webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Model
model = YOLO("v3.pt")

# MongoDB connection
MONGODB_URI = "mongodb+srv://magargame:Magarthai1@cluster0.msxpgo0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGODB_URI)
db = client.whitelist
whitelist_collection = db.list_whitelist

frame_count = 0
frame_interval = 10
check_old_value = ""

def distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    start_time = time.time()
    end_time = time.time()
    while GPIO.input(ECHO) == 0:
        start_time = time.time()
    while GPIO.input(ECHO) == 1:
        end_time = time.time()
    pulse_duration = end_time - start_time
    distance_cm = (pulse_duration * 34300) / 2
    return distance_cm

setup()
while True:
    success, img = cap.read()
    frame_count += 1

    if frame_count % frame_interval == 0:
        results = model(img, stream=True)
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)
        detected_objects = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = math.ceil((box.conf[0] * 100)) / 100
                cls = int(box.cls[0])
                class_name = classNames[cls]
                detected_objects.append((x1, class_name))
        detected_objects.sort(key=lambda x: x[0])
        detected_classes_string = "".join([obj[1] for obj in detected_objects])
        for x1, class_name in detected_objects:
            cv2.rectangle(img, (x1, y1), (x1 + 60, y1 + 30), (255, 0, 255), 3)
            draw.text((x1, y1), f"{class_name}", font=font, fill=(255, 0, 0))
        img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        cv2.imshow('Webcam', img)
         
        if GPIO.input(ir_sensor_pin) == GPIO.HIGH:
            print("Slot 1 clear")
        else:
            print("Slot 1 parking")

        dist = distance()
        print(dist)
        if 1 <= dist < 15:
            set_angle(90, pwm2)
        else:
            set_angle(0, pwm2)
        if len(detected_classes_string) > 0:
            data = {"license": detected_classes_string}
            print('data : ', detected_classes_string)
            result = whitelist_collection.find_one(data)
            check_old_value = detected_classes_string
            print(check_old_value)
            if result is not None:
                print(detected_classes_string, "Is Whitelisted!!!")
                set_angle(90, pwm)
                time.sleep(5)
            else:
                print(detected_classes_string, "Not Whitelisted!!!")
                set_angle(0, pwm)
        else:
            print("Not Found Anything!!!")
            set_angle(0, pwm)
   
    if cv2.waitKey(1) == ord('q'):
        break
