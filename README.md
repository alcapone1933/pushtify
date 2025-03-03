# Pushtify

Dieser Docker-Container basiert auf dem Pushtify-Projekt von [Sebastian Wüthrich](https://github.com/sebw/pushtify).

Das ursprüngliche Pushtify-Projekt ist ein Tool zum Weiterleiten von Gotify Benachrichtigungen an Pushover.

Diese Docker-Container leitet Gotify Benachrichtigungen an noch mehr Dienste per [shoutrrr](https://containrrr.dev/shoutrrr/latest/services/overview/) als python script.

### Docker CLI

```bash
docker run -dt \
    --restart always \
    --name pushtify \
    -e TZ=Europe/Berlin \
    -e "SHOUTRRR_URL=discord://123456abc@555555555555555" \
    -e GOTIFY_TOKEN=1234567890 \
    -e GOTIFY_URL=https://gotify.example.org \
    -e NOTIFY_FILE_SAVE=false \
    alcapone1933/pushtify:latest

```

### Docker Compose
```yaml
services:
  pushtify:
    image: alcapone1933/pushtify:latest
    container_name: pushtify
    restart: always
    tty: true
    # volumes:
      # - data:/app/data
    environment:
      - TZ=Europe/Berlin
      - "SHOUTRRR_URL=discord://123456abc@555555555555555"
      - GOTIFY_TOKEN=1234567890
      - GOTIFY_URL=http://192.168.178.16:80
      # - GOTIFY_URL=https://gotify.example.org
      - NOTIFY_FILE_SAVE=false
# volumes:
  # data:
```
* * *

## Volume Parameter

| Name (Beschreibung) #Optional | Wert    | Standard       |
| ----------------------------- | ------- | -------------- |
| Speicherort Json Nachrichten  | volume  | data:/app/data |

&nbsp;

## Env Parameter

| Name (Beschreibung)                                                   | Wert              | Standard           | Beispiel                            |
| --------------------------------------------------------------------- | ----------------- | ------------------ | ----------------------------------- |
| Zeitzone                                                              | TZ                | Europe/Berlin      | Europe/Berlin                       |
| Gotify client Token                                                   | GOTIFY_TOKEN      | ------------------ | 1234567890                          |
| Gotify url für den Server                                             | GOTIFY_URL        | ------------------ | http://192.168.178.16:80            |
| SHOUTRRR URL: Deine Shoutrrr URL z.b ( gotify,discord,telegram,email) | SHOUTRRR_URL      | ------------------ | discord://123456abc@555555555555555 |
| Nachrichten abspeichern in /app/data als json datei                   | NOTIFY_FILE_SAVE  | false              | false oder true                     |
