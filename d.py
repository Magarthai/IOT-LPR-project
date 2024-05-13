import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Set GPIO17 as the output pin
servo_pin = 17
GPIO.setup(servo_pin, GPIO.OUT)

# Create a PWM object with 50Hz frequency
pwm = GPIO.PWM(servo_pin, 50)

# Function to convert angle to duty cycle
def angle_to_duty_cycle(angle):
    duty_cycle = (angle / 18) + 2
    return duty_cycle

# Function to move the servo to a specific angle
def move_servo(angle):
    duty_cycle = angle_to_duty_cycle(angle)
    pwm.start(duty_cycle)
    time.sleep(1)  # Adjust sleep time as needed
    pwm.stop()

try:
    while True:
        # Move the servo from 0 to 180 degrees
        for angle in range(0, 181, 10):
            move_servo(angle)
            time.sleep(0.5)  # Adjust sleep time as needed

        # Move the servo from 180 to 0 degrees
        for angle in range(180, -1, -10):
            move_servo(angle)
            time.sleep(0.5)  # Adjust sleep time as needed

except KeyboardInterrupt:
    # Clean up GPIO on keyboard interrupt
    pwm.stop()
    GPIO.cleanup()
