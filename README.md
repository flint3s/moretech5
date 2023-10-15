## https://moretech.flint3s.ru/#/ - ссылка на веб-приложение

### Технологии, используемые в проекте: каждый раздел вынесен в отдельный микросервис
* ##### fastapi + mongoDB (Сервер)
* ##### Vue3 + naiveUI + Typescript (Клиент)
* ##### ClickHouse (Симуляция электронной очереди)

Для запуска всех микросервисов требуется указать переменные окружения и запустить docker-compose:
```
docker-compose up
```

Для CI/CD - GitHub Actions, Docker и Portainer 

<hr>
Решение было реализовано в рамках хакатона MORE.Tech 5.0 командой flint3s
