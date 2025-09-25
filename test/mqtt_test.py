import json
import time
import threading
from datetime import datetime
from awscrt import mqtt, http
from awsiot import mqtt_connection_builder

response_received = None
received_event = threading.Event()

# AWS IoT Core settings
AWS_ENDPOINT = "aekn458elx3wr-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "RaspberryPiClient"
TOPIC_PUB = "iot/data"
TOPIC_SUB = "iot/response"

CERT_PATH = "AWS_Creds/IoT_Device1.cert.pem"
KEY_PATH = "AWS_Creds/IoT_Device1.private.key"
CA_PATH = "AWS_Creds/root-CA.crt"

mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=AWS_ENDPOINT,
    cert_filepath=CERT_PATH,
    pri_key_filepath=KEY_PATH,
    ca_filepath=CA_PATH,
    client_id="TestClient123",
    clean_session=True,
    keep_alive_secs=30
)

mqtt_connection.connect().result()
print("Connected!")
mqtt_connection.disconnect().result()
