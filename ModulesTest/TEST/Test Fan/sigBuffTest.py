import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
FAN_PIN = 24
GPIO.setup(FAN_PIN, GPIO.OUT)
GPIO.output(FAN_PIN, False)