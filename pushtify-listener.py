import websocket
import json
import os
import subprocess
from datetime import datetime

shoutrrr_url = os.environ['SHOUTRRR_URL']
gotify_url = os.environ['GOTIFY_URL']
gotify_token = os.environ['GOTIFY_TOKEN']
notify_file_save = os.environ.get('NOTIFY_FILE_SAVE', 'false').lower() == 'true'  # Standardmäßig auf False setzen

def send_with_shoutrrr_url(message, title):
    # Extrahiere den Service aus der SHOUTRRR_URL
    service = shoutrrr_url.split("://")[0] if "://" in shoutrrr_url else "Unknown"

    # Erzeuge den Befehl
    command = ["/usr/local/bin/shoutrrr", "send", "-v", "--url", shoutrrr_url, "--message", message, "--title", title]

    # Führe den Befehl aus
    subprocess.run(command)

    # Drucke den Service in der Ausgabe
    print(f"Notification sent | Service: {service}")

def process_notification(msg):
    # Extrahiere Informationen aus der Benachrichtigung
    notification_id = msg.get('id', 'N/A')
    app_id = msg.get('appid', 'N/A')
    message = msg.get('message', 'N/A')
    title = msg.get('title', 'N/A')
    priority = msg.get('priority', 'N/A')
    timestamp = msg.get('date', 'N/A')

    # Drucke die Informationen im gewünschten Format
    print(f"Timestamp: {timestamp}")
    print(f"Notification ID: {notification_id}")
    print(f"App ID: {app_id}")
    print(f"Priority: {priority}")
    print(f"Title: {title}")
    print(f"Message: {message}")

    # Sende die Benachrichtigung über Shoutrrr
    send_with_shoutrrr_url(message, title)

    # Speichere die JSON-Nachricht in einer Datei mit Timestamp, wenn notify_file_save True ist
    if notify_file_save:
        save_filename = f"notification_{timestamp.replace(':', '').replace('+', '').replace('.', '')}.json"
        with open(save_filename, 'w') as json_file:
            json.dump(msg, json_file, indent=2)
        print(f"Saved JSON to: {save_filename}")

def on_message(ws, message):
    try:
        msg = json.loads(message)
        process_notification(msg)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    
    print(f"Received message: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"### closed ### | Status code: {close_status_code} | Message: {close_msg}")

def on_open(ws):
    print("Opened connection")

if __name__ == "__main__":
    if "http://" in gotify_url:
        ws_url = f"ws://{gotify_url.split('http://')[1]}/stream"
    elif "https://" in gotify_url:
        ws_url = f"wss://{gotify_url.split('https://')[1]}/stream"
    else:
        print("Invalid GOTIFY_URL format. Please include 'http://' or 'https://' in the GOTIFY_URL variable.")
        exit(1)

    wsapp = websocket.WebSocketApp(ws_url, header={"X-Gotify-Key": str(gotify_token)},
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    wsapp.run_forever()
