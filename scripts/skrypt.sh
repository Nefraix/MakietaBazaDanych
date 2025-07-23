#!/bin/bash

VENV_PYTHON="/home/pi/MakietaBazaDanych/venv/bin/python3"
APP_PATH="/home/pi/MakietaBazaDanych/API/fastapi_app.py"

get_ip(){
	hostname -I | awk '{print $1}' | grep -v "^127"
}

while true; do
	ip=$(get_ip)
	if [ -n "$ip" ]; then
		echo "IP acquired: $ip"
		break
	fi
	echo "Waiting..."
	sleep 2
done


usedPort=8040
logFile=~/Desktop/BazaInfo.txt

echo "$ip" > "$logFile"
echo "$usedPort" >> "$logFile"


$VENV_PYTHON -m uvicorn API.fastapi_app:app --host 0.0.0.0 --port $usedPort --reload --app-dir /home/pi/MakietaBazaDanych
