# 🔁 Barter Platform API

Платформа для обмена вещами между пользователями. Реализована на Django + DRF, с использованием JWT авторизации и PostgreSQL в Docker.

---

## ⚙️ Технологии

- Python 3.11+
- Django 5.2
- Django REST Framework
- PostgreSQL (Docker)
- JWT авторизация (SimpleJWT)
- Docker + Docker Compose
- Unittest (DRF test framework)

---

## 🚀 Быстрый старт

### 1. Клонирование и запуск

```bash
git clone https://github.com/your_username/barter.git
cd barter
docker-compose up --build -d
```
### 2. Миграции и суперпользователь
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```
### 3. Админка
```bash
http://localhost:8000/admin/
```

## 🔐 JWT авторизация
Получить токен
```http
POST /api/token/
```

Тело запроса:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

Обновить токен
```http
POST /api/token/refresh/
```

## 📚 Эндпоинты API
### Объявления (`/api/ads/`)

| Метод  | URL                         | Описание                           |
|--------|-----------------------------|------------------------------------|
| GET    | `/api/ads/`                 | Список объявлений                  |
| POST   | `/api/ads/`                 | Создать объявление                 |
| PATCH  | `/api/ads/<id>/`            | Обновить своё объявление           |
| DELETE | `/api/ads/<id>/`            | Удалить своё объявление            |
| GET    | `/api/ads/?search=abc`      | Поиск по title/description         |
| GET    | `/api/ads/?category=X`      | Фильтрация по категории            |
| GET    | `/api/ads/?condition=Y`     | Фильтрация по состоянию            |

🧪 Запуск тестов
```bash
docker-compose exec web python manage.py test 
```

📁 Структура проекта
``` bash
barter_project/
├── ads/
│   ├── models.py          # Ad, ExchangeProposal
│   ├── views.py           # ViewSet-ы (Ad, ExchangeProposal)
│   ├── serializers.py     # DRF сериализаторы
│   ├── urls.py            # router-ы для API
│   ├── tests.py           # модульные тесты
├── barter_project/
│   ├── settings.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
```
# 🛡 Особенности безопасности
Все API требуют JWT авторизации (IsAuthenticated)

Только автор может изменять или удалять своё объявление

Только получатель предложения (ad_receiver.user) может принять или отклонить его