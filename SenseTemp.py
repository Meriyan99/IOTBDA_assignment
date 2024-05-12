# Import essential packages.

import time

import Adafruit_DHT #Module necassarily needed to use DHT sensor.

import RPi.GPIO as GPIO #Module used to manipulate general purpose input and output.
GPIO.setmode(GPIO.BCM)

# Function to sense temperature through DHT11
def observeTemp(sensor, pin):
    
    print("------------Starting to read temperature--------------")
    # Pass the type of sensor and respective pin of sensor connected to raspberyy pi.
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is None and temperature is None:
        humidity, temperature = None
    else:
        humidity = round(humidity,2)
        temperature = round(temperature,2)
        
    return humidity,temperature