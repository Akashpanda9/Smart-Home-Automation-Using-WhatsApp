from flask import Flask, request
import RPi.GPIO as GPIO

# Initialize Flask app
app = Flask(__name__)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)  # Replace 18 with your GPIO pin

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    body = request.form.get("Body").lower()
    if "on" in body:
        GPIO.output(18, GPIO.HIGH)  # Turns on the LED
        response = "Fan turned on"
    elif "off" in body:
        GPIO.output(18, GPIO.LOW)   # Turns off the LED
        response = "Fan turned off"
    else:
        response = "Invalid command"
    
    return str('<?xml version="1.0" encoding="UTF-8"?>'
               '<Response><Message>' + response + '</Message></Response>')

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
