import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor control pins
ENA = 18    # Enable pin
IN1 = 22    # Input 1
IN2 = 23    # Input 2

# Setup pins
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

# Enable the motor driver
GPIO.output(ENA, GPIO.HIGH)

try:
    print("Motor Forward")
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    time.sleep(5)

    print("Motor Backward")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    time.sleep(5)

    print("Motor Stop")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)

except KeyboardInterrupt:
    print("Stopped by User")

finally:
    GPIO.cleanup()