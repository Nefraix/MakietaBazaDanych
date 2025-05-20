#!/bin/bash

ip4=$(hostname -I)
usedPort=8040


echo "("IP RPI: $ip4")"
echo "("Port: $usedPort")"

echo $ip4 > ~/Desktop/BazaInfo.txt
echo $usedPort >> ~/Desktop/BazaInfo.txt

rm items.db

uvicorn fastapi_app:app --host 0.0.0.0 --port $usedPort --reload

