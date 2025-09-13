# nginx-router/Dockerfile

# Stage 1: Build
FROM node:22-alpine3.22 AS build
WORKDIR /app
COPY frontend/package.json frontend/yarn.lock ./
ENV PATH=/app/node_modules/.bin:$PATH
COPY frontend/ ./
RUN yarn install --frozen-lockfile
RUN yarn build

# Stage 2: Serve with nginx
FROM nginx:latest

COPY --from=build /app/dist /usr/share/nginx/html
# Скопируйте ваш файл конфигурации nginx.conf в контейнер
COPY nginx-router/tamerun.conf /etc/nginx/conf.d/tamerun.conf

# Откройте порт, который будет слушать ваш NGINX внутри контейнера
EXPOSE 80
EXPOSE 443

# Опционально: скопируйте MIME types, если они вам нужны и не включены по умолчанию
# COPY mime.types /etc/nginx/mime.types

# Команда для запуска NGINX в foreground режиме (важно для Docker)
CMD ["nginx", "-g", "daemon off;"]
