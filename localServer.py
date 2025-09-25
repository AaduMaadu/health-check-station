# main.py

import time
import json
import adafruit_dht
import board
from gpiozero import LED, Button
from tinydb import TinyDB
from aws_mqtt_handler import setup_mqtt, publish_data, get_response

# GPIO setup
dht_device = adafruit_dht.DHT11(board.D4)
button = Button(21)
led1 = LED(27)  # Stall and Success
led2 = LED(17)  # Fail
led3 = LED(22)  # Button status

# User and DB
userId = "IoTUser1"
db = TinyDB('db.json')

# MQTT
mqtt_connection = setup_mqtt()
response = None

def getDHTData():
    try:
        temp_c = dht_device.temperature
        temp_f = temp_c * (9 / 5) + 32
        print("Temp: {:.1f} F".format(temp_f))
        return temp_f
    except RuntimeError as err:
        print("Sensor error:", err.args[0])
        return None


while True:
    if button.is_pressed:
        print("Button pressed.")
        led3.on()

        # Stall indicator (blink)
        for _ in range(5):
            temp = getDHTData()
            db.insert({'temp': stable_temp, 'userId': userId}) # Save to DB
            publish_data(mqtt_connection, userId, temp) # Publish to AWS
            led1.on()
            time.sleep(0.5)
            led1.off()
            time.sleep(0.5)

        # Wait for response
        for i in range(5):
            response = get_response()
            
            if response is not None:
                break
                
            print(f"No response, attemptting again {i}")
            led2.on()
            time.sleep(0.5)
            led2.off()
                
        led3.off()

        if response == "GOOD":
            print("AWS response: GOOD")
            led1.on()
            time.sleep(5)
            led1.off()
        else:
            print("AWS response: BAD or timeout")
            led2.on()
            time.sleep(5)
            led2.off()

    time.sleep(1)
    
    #stable_temp = getDHTData()
    #db.insert({'temp': stable_temp, 'userId': userId})
    #publish_data(mqtt_connection, userId, stable_temp)
