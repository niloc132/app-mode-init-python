FROM ghcr.io/deephaven/server AS init-server
COPY app.d /app.d

FROM ghcr.io/deephaven/web AS init-web
COPY data/layouts /data/layouts
RUN chown www-data:www-data /data/layouts
