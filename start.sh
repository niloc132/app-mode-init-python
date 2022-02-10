docker build --target init-server --tag deephaven-examples/app-mode-init-python .
docker build --target init-web --tag deephaven-examples/app-mode-init-python-web .
docker-compose up $1
