# aws_mqtt_handler.py

import json
import time
import threading
from datetime import datetime
from awscrt import mqtt, http
from awsiot import mqtt_connection_builder

# AWS IoT Core settings
AWS_ENDPOINT = "aekn458elx3wr-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "RaspberryPiClient"
TOPIC_PUB = "iot/data"
TOPIC_SUB = "iot/response"

CERT_PATH = "AWS_Creds/IoT_Device1.cert.pem"
KEY_PATH = "AWS_Creds/IoT_Device1.private.key"
CA_PATH = "AWS_Creds/root-CA.crt"

response_received = None
received_event = threading.Event()

def on_message_received(topic, payload, **kwargs):
    global response_received
    response_received = payload.decode()
    print(f"Received from AWS: {response_received}")
    received_event.set()

def setup_mqtt():
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=AWS_ENDPOINT,
        port=8883,
        cert_filepath=CERT_PATH,
        pri_key_filepath=KEY_PATH,
        ca_filepath=CA_PATH,
        client_id=CLIENT_ID,
        clean_session=False,
        keep_alive_secs=30)
	
	#print(f"Connecting to {AWS_ENDPOINT} with client ID '{CLIENT_ID}'...")
    mqtt_connection.connect().result()
    print("Connected!")
    
    #Susbscribe
    print("Subscribing to topic '{}'...".format(TOPIC_SUB))
    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=TOPIC_SUB,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received)
    
    subscribe_result = subscribe_future.result()
    print("Subscribed with {}".format(str(subscribe_result['qos'])))

    return mqtt_connection

def publish_data(mqtt_connection, userId, temp):
    timestamp = datetime.utcnow().isoformat() + "Z"
    payload = {
        "userId": userId,
        "temp": temp,
        "timestamp": timestamp
    }
    message_json = json.dumps(payload)
    print(f"Publishing to AWS: {message_json}")
    mqtt_connection.publish(
        topic=TOPIC_PUB,
        payload=message_json,
        qos=mqtt.QoS.AT_LEAST_ONCE
    )

def get_response(timeout=5):
    global response_received
    response_received = None
    received_event.clear()
    if received_event.wait(timeout):
        return response_received
    else:
        return None
