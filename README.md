Инструкция по запуску:

1. Установите Docker: https://www.docker.com/products/docker-desktop/
2. Скопируйте папку проекта на свой компьютер
3. Откройте терминал в папке проекта
4. Выполните команды:
   docker build -t gpt-frontend .
   docker run -p 5001:5000 gpt-frontend
5. Откройте в браузере http://localhost:5001
6. Введите ваш API ключ от сервиса