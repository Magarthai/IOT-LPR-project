import RPi.GPIO as GPIO

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins for the sensors
sensor_pins = {
    "sensor1": 26,
    "sensor2": 19,
    "sensor3": 20,
    "sensor4": 16
}

# Initialize a dictionary to hold counts for each sensor
sensor_counts = {sensor: 0 for sensor in sensor_pins}

# Set up GPIO pins as inputs
for sensor, pin in sensor_pins.items():
    GPIO.setup(pin, GPIO.IN)

try:
    while True:
        # Read the values of each sensor and update counts
        for sensor, pin in sensor_pins.items():
            if GPIO.input(pin) == GPIO.HIGH:
                sensor_counts[sensor] += 1
                print(f"{sensor} IR code is high. Count: {sensor_counts[sensor]}")

finally:
    # Clean up GPIO
    GPIO.cleanup()
