#!/usr/bin/env bash

# Define cleanup procedure
cleanup() {
    echo "================================ STOP GOTIFY NOTIFY FORWARDER ==============================="
}

# Trap SIGTERM
trap 'cleanup' SIGTERM
echo "================================ START GOTIFY NOTIFY FORWARDER ==============================="
ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

echo "YOUR GOTIFY Website: $GOTIFY_URL"
echo -e "Waiting for Healthcheck...\n"
sleep 5
wait_for_healthcheck() {
    until curl -k -f "$GOTIFY_URL/health" >/dev/null 2>&1; do
        echo -e "Waiting for Healthcheck...\n"
        sleep 5
    done
    echo -e "\nHealthcheck successful! Website is reachable ."
}

# Warte auf den Healthcheck, bevor der Hauptbefehl ausgeführt wird
wait_for_healthcheck

set /usr/bin/python3 /usr/local/bin/pushtify-listener.py "$@"
exec "$@" &

wait $!
