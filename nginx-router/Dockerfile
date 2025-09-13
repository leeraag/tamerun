# nginx-router/Dockerfile

FROM nginx:latest

# Скопируйте ваш файл конфигурации nginx.conf в контейнер
COPY conf.d /etc/nginx/conf.d

# Откройте порт, который будет слушать ваш NGINX внутри контейнера
EXPOSE 80
EXPOSE 443

# Опционально: скопируйте MIME types, если они вам нужны и не включены по умолчанию
# COPY mime.types /etc/nginx/mime.types

# Команда для запуска NGINX в foreground режиме (важно для Docker)
CMD ["nginx", "-g", "daemon off;"]