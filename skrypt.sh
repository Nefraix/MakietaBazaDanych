#!/bin/bash

ip4=$(hostname -I | awk '{print $1}')
usedPort=8040
logFile=~/Desktop/BazaInfo.txt

echo "$ip4" > "$logFile"
echo "$usedPort" >> "$logFile"


uvicorn fastapi_app:app --host 0.0.0.0 --port $usedPort --reload

