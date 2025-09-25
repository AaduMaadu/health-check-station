# mqtt_handler.py

import json
import ssl
import paho.mqtt.client as mqtt
import time
import os

AWS_ENDPOINT = "aekn458elx3wr-ats.iot.us-east-2.amazonaws.com" 
CLIENT_ID = "RaspberryPiClient"
TOPIC_PUB = "iot/data"
TOPIC_SUB = "iot/response"

ca_certs = "AWS_Creds/root-CA.crt"
certfile = "AWS_Creds/IoT_Device1.cert.pem"
keyfile = "AWS_Creds/IoT_Device1.private.key"

for path in [ca_certs, certfile, keyfile]:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Missing file: {path}")

response_received = None

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
    else:
        print:(f"Connected fail with code {rc}")


def on_message(client, userdata, msg):
    global response_received
    response_received = msg.payload.decode()
    print("Received from AWS:", response_received)


def setup_mqtt():
    mqtt_client = mqtt.Client(client_id=CLIENT_ID)
    mqtt_client.tls_set(
        ca_certs = ca_certs,
        certfile = certfile,
        keyfile = keyfile,
        tls_version=ssl.PROTOCOL_TLSv1_2
    )
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.will_set('raspberry/status', b'{"status": "Off"}') # Set the will message, when the Raspberry Pi is powered off, or the network is interrupted abnormally, it will send the will message to other clients
    mqtt_client.connect(AWS_ENDPOINT, 8883, 60)
    mqtt_client.subscribe(TOPIC_SUB)
    mqtt_client.loop_start()
    return mqtt_client

iot
def publish_data(mqtt_client, userId, temp):
    payload = json.dumps({'userId': userId, 'temp': temp})
    mqtt_client.publish(TOPIC_PUB, payload, qos=1)
    print("Published to AWS:", payload)


def get_response():
    global response_received
    response_received = None
    wait_start = time.time()
    while response_received is None and time.time() - wait_start < 5:
        time.sleep(0.5)
    return response_received
