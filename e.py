import RPi.GPIO as GPIO
import time

# GPIO pins
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

if __name__ == '__main__':
    try:
        setup()
        while True:
            dist = distance()
            print("Distance: %.1f cm" % dist)
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
