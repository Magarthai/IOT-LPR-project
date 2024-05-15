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
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set the frame width to 640 pixels
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set the frame height to 480 pixels

# Model
model = YOLO("v3.pt")

# MongoDB connection
MONGODB_URI = "mongodb+srv://magargame:Magarthai1@cluster0.msxpgo0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGODB_URI)
db = client.whitelist
whitelist_collection = db.list_whitelist

import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin for the servo
servo_pin = 27
servo2_pin = 25
ir_sensor_pin1 = 26
ir_sensor_pin2 = 19
ir_sensor_pin3 = 20
ir_sensor_pin4 = 16
buzzer_pin = 23
# Set PWM parameters
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(servo2_pin, GPIO.OUT)
GPIO.setup(ir_sensor_pin1, GPIO.IN)
GPIO.setup(ir_sensor_pin2, GPIO.IN)
GPIO.setup(ir_sensor_pin3, GPIO.IN)
GPIO.setup(ir_sensor_pin4, GPIO.IN)
GPIO.setup(buzzer_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50) # 50 Hz (20 ms PWM period)
pwm2 = GPIO.PWM(servo2_pin, 50) # 50 Hz (20 ms PWM period)
# Function to convert angle to duty cycle
def angle_to_duty_cycle(angle):
    duty_cycle = (angle / 18) + 2
    return duty_cycle
def checkIR():
    full = 4
    if GPIO.input(ir_sensor_pin1) == GPIO.HIGH:
        full -= 1
    elif GPIO.input(ir_sensor_pin2) == GPIO.HIGH:
        full -= 1
    elif GPIO.input(ir_sensor_pin3) == GPIO.HIGH:
        full -= 1
    elif GPIO.input(ir_sensor_pin4) == GPIO.HIGH:
        full -= 1
    return full



# Function to move the servo to a specific angle
def set_angle(angle):
    duty_cycle = angle_to_duty_cycle(angle)
    pwm.start(duty_cycle)
    time.sleep(1) # Wait for the servo to reach the position
    
def set_angle2(angle):
    duty_cycle = angle_to_duty_cycle(angle)
    pwm2.start(duty_cycle)
    time.sleep(1) # Wait for the servo to reach the position
TRIG = 6
ECHO = 5

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

def distance():
    # Set trigger to HIGH
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start_time = time.time()
    end_time = time.time()

    # Wait for the echo to start
    while GPIO.input(ECHO) == 0:
        start_time = time.time()

    # Wait for the echo to end
    while GPIO.input(ECHO) == 1:
        end_time = time.time()

    # Calculate pulse duration
    pulse_duration = end_time - start_time

    # Speed of sound = 343m/s = 34300cm/s = 0.0343cm/µs
    # Distance = (Time * Speed)/2
    distance_cm = (pulse_duration * 34300) / 2

    return distance_cm
    
# Object classes
classNames = ['0', '1', 'ก', 'ข', 'ค', 'ฆ', 'ง', 'จ', 'ฉ', 'ช', 'ฌ', 'ญ', '2', 'ฎ', 'ฐ', 'ฒ', 'ณ', 'ด', 'ต', 'ถ', 'ท', 'ธ', 'น', '3', 'บ', 'ผ', 'พ', 'ฟ', 'ภ', 'ม', 'ย', 'ร', 'ล', 'ว', '4', 'ศ', 'ษ', 'ส', 'ห', 'ฬ', 'อ', 'ฮ', '5', '6', '7', '8', '9']

# Load Thai font
font_path = "Kanit-Medium.ttf"  # Change to the path where your Thai font is located
font = ImageFont.truetype(font_path, 20)

frame_count = 0
frame_interval = 10  # Adjust as needed

check_old_value = ""
global_check = False
setup()
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
        

        IR_active = checkIR()
        inactive_IR = 4 - IR_active

        dist = distance()
        print(dist)
        if 1 <= dist < 15:
            set_angle2(90)
        else:
            set_angle2(0)
        IR_active = checkIR()
        
        if inactive_IR > 0 :
            if len(detected_classes_string) > 0:
                data = {"license": detected_classes_string}
                print('data : ', detected_classes_string)
                result = whitelist_collection.find_one(data)
                check_old_value = detected_classes_string
                print(check_old_value)
                if result is not None:
                    print(detected_classes_string, "Is Whitelisted!!!")
                    global_check = True
                    set_angle(90)
                    time.sleep(5)
    
                else:
                    print(detected_classes_string, "Not Whitelisted!!!")
                    global_check = True
                    set_angle(0)
            else:
                print("Not Found Anything!!!")
                set_angle(0)
        else:
            print("Full slot!!!")
            for _ in range(2):
                GPIO.output(buzzer_pin, GPIO.HIGH)  # Turn buzzer on
                time.sleep(0.5)  # Beep for 0.5 seconds
                GPIO.output(buzzer_pin, GPIO.LOW)  # Turn buzzer off
                time.sleep(0.5)  # Wait for 0.5 seconds between beeps
            set_angle(0)
            
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
