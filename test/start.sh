#!/usr/bin/env bash
# stop script on error
set -e

# Check for python 3
if ! python3 --version &> /dev/null; then
  printf "\nERROR: python3 must be installed.\n"
  exit 1
fi

# Check to see if root CA file exists, download if not
if [ ! -f ./root-CA.crt ]; then
  printf "\nDownloading AWS IoT Root CA certificate from AWS...\n"
  curl https://www.amazontrust.com/repository/AmazonRootCA1.pem > root-CA.crt
fi

# run pub/sub sample app using certificates downloaded in package
printf "\nRunning pub/sub sample application...\n"
python3 pubsub1.py --endpoint aekn458elx3wr-ats.iot.us-east-1.amazonaws.com --ca_file AWS_Creds/root-CA.crt --cert AWS_Creds/IoT_Device1.cert.pem --key AWS_Creds/IoT_Device1.private.key --client_id basicPubSub --topic sdk/test/python --count 0
