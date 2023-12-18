FROM alcapone1933/alpine:latest
RUN apk add --update --no-cache tzdata curl bash tini jq py3-pip && pip3 install --break-system-packages websocket-client rel && \
    rm -rf /var/cache/apk/* && \
    mkdir -p /app/data

WORKDIR /app/data

LABEL maintainer="alcapone1933 <alcapone1933@cosanostra-cloud.de>" \
      org.opencontainers.image.created="$(date +%Y-%m-%d\ %H:%M)" \
      org.opencontainers.image.authors="alcapone1933 <alcapone1933@cosanostra-cloud.de>" \
      org.opencontainers.image.url="https://hub.docker.com/r/alcapone1933/pushtify" \
      org.opencontainers.image.version="v0.0.1" \
      org.opencontainers.image.ref.name="alcapone1933/pushtify" \
      org.opencontainers.image.title="Gotify forwarder with shoutrrr" \
      org.opencontainers.image.description="Listen for Gotify notifications over websocket and forward them with shoutrrr."

ENV TZ=Europe/Berlin \
    VERSION="v0.0.1" \
    SHOUTRRR_URL="" \
    GOTIFY_TOKEN="xyz" \
    GOTIFY_URL="http://gotify.example.org"

COPY --chmod=0755 pushtify-listener.py entrypoint.sh /usr/local/bin
COPY --from=alcapone1933/shoutrrr:latest /usr/local/bin/shoutrrr /usr/local/bin/shoutrrr
# ENTRYPOINT ["python3","/usr/local/bin/pushtify-listener.py"]
ENTRYPOINT ["/sbin/tini", "--", "/usr/local/bin/entrypoint.sh"]
