# Import necassary modules

import time
import paho.mqtt.client as paho # Client used in connecting to an MQTT Broker.
from paho import mqtt
import Adafruit_DHT # Module necassarily needed to use DHT sensor.
import RPi.GPIO as GPIO # Module used to manipulate general purpose input and output

from SenseTemp import observeTemp #Import function to sense environment temperature.

GPIO.setmode(GPIO.BCM)

sensor = Adafruit_DHT.DHT11 # Initializing the sensor.
pin = 4 # GPIO pin 4 of raspberry pi is connected with sensor.
sensor_data = {'temperature' : 0, 'humidity' : 0} # The sensor data recieved is saved as a dictionary.

#-------------------------------------------------- INITIATING A SELF HOSTED MQTT MANAGEMENT ------------------------------------------------

# Setting callback for events to check connection.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# Setting callback to check if publisher is working.
def on_publish(client, userdata, mid, properties=None):
    print("Published mid: " + str(mid))
    
#----------------------------------------------------------------------------------------------
mqtt_broker = "broker.hivemq.com"  # Defining the self hosted broker used.
mqtt_port = 1883 # Mqtt broker access port.

mqtt_topic = "Group11/Temperature" # Defining the MQTT topic used.

#----------------------------------------------------------------------------------------------

#instantiate the client with parameters.
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5) # Defining the paho client.
client.on_connect = on_connect

# connect the client to HiveMQ
client.connect(mqtt_broker, mqtt_port)

# Setting callback on publishing.
client.on_publish = on_publish

client.loop_start()

#----------------------------------------------------------------------------------------------

# Publish
#----------------------------------------------------------------------------------------------
while True:
    humidity,temperature = observeTemp(sensor, pin) # call the imported function defined.
    if humidity is None and temperature is None:
        print("Failed to get reading. Try Again")
    else:
        print("Temperature={0:0.1f}*C Humidity={1:0.2f}%".format(temperature,humidity)) # Obtaining the sensed temperature.
        client.publish(mqtt_topic, payload= str(temperature), qos=1) # Publishing the temperature sensed to the MQTT topic defined.
        
    time.sleep(1) # Sleep time for the next iteration.


# Client loop stops only when done manually.
# client.loop_forever()
