from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import RPi.GPIO as GPIO
from signal import signal, SIGINT
from sys import exit

app = Flask(__name__)

# ---------------- GPIO Setup ---------------- #

LED_PIN = 17

ENA = 18
IN1 = 22
IN2 = 23

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

# Enable Motor Driver
GPIO.output(ENA, GPIO.HIGH)


# ---------------- Cleanup Function ---------------- #

def cleanup_gpio(signal_received=None, frame=None):
    print("\nCleaning up GPIO...")

    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(ENA, GPIO.LOW)

    GPIO.cleanup()
    exit(0)


signal(SIGINT, cleanup_gpio)


# ---------------- WhatsApp Bot ---------------- #

@app.route("/bot", methods=["POST"])
def bot():

    msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()

    if "light on" in msg:
        GPIO.output(LED_PIN, GPIO.HIGH)
        resp.message("💡 Light is ON")

    elif "light off" in msg:
        GPIO.output(LED_PIN, GPIO.LOW)
        resp.message("💡 Light is OFF")

    elif "fan on" in msg:
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        resp.message("🌀 Fan is ON")

    elif "fan off" in msg:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        resp.message("🌀 Fan is OFF")

    else:
        resp.message(
            "Available Commands:\n\n"
            "light on\n"
            "light off\n"
            "fan on\n"
            "fan off"
        )

    return str(resp)


# ---------------- Run Server ---------------- #

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )