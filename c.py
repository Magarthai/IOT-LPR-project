import RPi.GPIO as GPIO
import time

# Set GPIO mode to Broadcom SOC numbering
GPIO.setmode(GPIO.BCM)

# Set GPIO17 as output
GPIO.setup(17, GPIO.OUT)

# Create PWM instance with frequency 50Hz
pwm = GPIO.PWM(17, 50)

# Start PWM with duty cycle corresponding to 90 degrees
pwm.start(7.5)

try:
    while True:
        # Change the duty cycle to rotate the servo
        pwm.ChangeDutyCycle(7.5)  # For 90 degrees
        time.sleep(1)  # Adjust sleep time as needed
except KeyboardInterrupt:
    # Clean up GPIO on keyboard interrupt
    pwm.stop()
    GPIO.cleanup()
