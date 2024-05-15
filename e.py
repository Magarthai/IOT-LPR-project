import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin for the buzzer
buzzer_pin = 23

# Set up buzzer pin as output
GPIO.setup(buzzer_pin, GPIO.OUT)

try:
    # Beep twice with a frequency of 1 Hz
    for _ in range(2):
        GPIO.output(buzzer_pin, GPIO.HIGH)  # Turn buzzer on
        time.sleep(0.5)  # Beep for 0.5 seconds
        GPIO.output(buzzer_pin, GPIO.LOW)  # Turn buzzer off
        time.sleep(0.5)  # Wait for 0.5 seconds between beeps

finally:
    # Clean up GPIO
    GPIO.cleanup()
