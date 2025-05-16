Платформа для онлайн обучения, на которой каждый желающий может размещать свои полезные материалы или курсы

Проект реализован на Django с поддержкой Docker, PostgreSQL, Redis, Celery и Celery Beat

## Установка и настройка

1. Установите Docker и Docker Compose 

2. Скопируйте файл .env.example в .env и заполните требуемые значения

3. Запустите проект командой "docker compose up -d --build"

## Деплой на сервер 
1. Войдите на сервер 
2. Скопируйте проект командой git clone https://github.com/TamirMandreev/lms_project.git
3. Создайте файл .env и заполните требуемые значения, опираясь на файд .env.example
4. Запустите контейнеры в режиме демона: sudo docker compose up -d
5. Проверьте работу контейнеров: sudo docker compose ps