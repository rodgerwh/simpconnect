# Эндпоинты API

POST /api/clients/create/
- Создание пользователя
- Пример запроса: {
    "email": "test1@mail.com",
    "password": "test",
    "first_name": "name",
    "last_name": "surname",
    "latitude": null,
    "longitude": null,
    "gender": null,
    "profile_picture": null
}
- Возвращает токен пользователя

POST /api/clients/auth-token/
- Возвращает токен пользователя, принимает username и password
- Пример запроса: {
    "username": "test1@mail.com",
    "password": "test"
}
- Пример ответа: {"token":"26b2f01db807eff4b7eca44ae7a8fce0b7f29c6f"}

POST /api/clients/{id}/match/
- Лайкает пользователя {id}, требуется токен авторизации в HEADERS запроса: Authorization Token {token}
- Пример запроса: POST запрос на /api/clients/1/match/, в Headers запроса ключ "Authorization" со значением "Token 26b2f01db807eff4b7eca44ae7a8fce0b7f29c6f"
- Пример ответа: {"success":"User liked successfully"}

GET /api/list/
- Возвращает список пользователей, требуется токен авторизации
- Параметры:
  first_name - фильтр по имени
  last_name - по фамилии
  gender - по полу, значения MALE, FEMALE, UNKNOWN
  distance - пользователи в пределах указанной дистанции
- Пример запроса: /api/list/?gender=MALE
