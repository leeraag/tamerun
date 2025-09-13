Развёртывание на сервере:
0. Перейти в рабочую директорию
`cd /home`
1. Склонировать репозиторий
`https://github.com/leeraag/tamerun.git`
(или через ssh)
2. Перейти в рабочую директорию проекта
`cd ./tamerun`
3. Переключиться на нужную ветку
`git switch release_1.1`
4. Создать директория для монтирования сертификата SSL
`mkdir -p ./certbot/conf ./certbot/www`
5. Запустить проект
`docker-compose up -d --build`
6. Сгенерировать сертификат вручную, вызвав команду внутри контейнера cerbot
`docker compose run --rm certbot certonly --webroot -w /var/www/certbot -d tamerun-invest.ru -d tamerun-invest.ru --email sap@grad1.ru  --agree-tos --no-eff-email`
(при отладке добавить флаг --staging, генерирующий временный сертификат без шифрования, но без лимитов)
Автоматический запуск блока `command` в сервисе `cerbot` не увенчался успехом. Команда воспринимается как имя файл и возникает ошибка по отсутствию такого файла. Ошибку возможно устранить, но в связи с ограниченными ресурсами выбран путь временного использования ручной генерации сертификата.
В случае падения сервиса nginx-router - временно закомментировать блок с server для 443 в конфигурации nginx `./nginx-router/tamerun.conf` и перезапустить контейнер `docker-compose up -f nginx-router`
7. После успешной генерации сертификата (в `./certbot/conf` появились файлы) раскоментировать в конфигурации nginx `./nginx-router/tamerun.conf` строки:
`#    ssl_certificate /etc/letsencrypt/live/tamerun-invest.ru/fullchain.pem;`
`#    ssl_certificate_key /etc/letsencrypt/live/tamerun-invest.ru/privkey.pem;`
и блок с server для 443, если комментировался.
8. Установить задачу по расписанию для обновления сертификата SSL 12 часов:
Открыть задачи текущего пользователя `cronab -e`
Добавить в конец задачу `0 */12 * * *   (docker-compose -f /home/tamerun/docker-compose.yml run --rm certbot renew --webroot -w /var/www/certbot && /home/tamerun/scripts/renew_nginx.sh) || echo "Certbot renew or Nginx reload failed."`
9. Для большей безопасности можно настроить сильные SSL Cipher Suites и сгенерируйте сильные DH параметры (с ходу настроить не вышло):
В каталог `./cerbot/conf` добавить файл `options-ssl-nginx.conf` с конфигурацией, например, отсюда https://ssl-config.mozilla.org/#server=nginx&version=1.27.3&config=intermediate&openssl=3.4.0&guideline=5.7
Туда же сгенерировать `ssl-dhparams.pem` командой `openssl dhparam -out ./certbot/conf/ssl-dhparams.pem 2048` # Или 4096 для большей безопасности
Раскоментировать пути к конфигам в конфигурации nginx и перезапустить контейнер