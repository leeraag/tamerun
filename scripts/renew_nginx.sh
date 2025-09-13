#!/bin/bash

# Ищем PID Nginx контейнера
NGINX_PID=$(docker inspect -f '{{.State.Pid}}' tamerun_nginx)

if [ -n "$NGINX_PID" ]; then
    # Перезагружаем конфигурацию Nginx
    echo "Reloading Nginx configuration..."
    kill -HUP $NGINX_PID
    echo "Nginx configuration reloaded."
else
    echo "Nginx container not found or not running."
fi
