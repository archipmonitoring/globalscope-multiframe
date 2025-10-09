# Документація API GlobalScope MultiFrame 11.0

*Документація також доступна англійською мовою: [api_documentation.md](api_documentation.md)*

# Документація API GlobalScope MultiFrame 11.0

## Огляд
Цей документ надає комплексну документацію для API GlobalScope MultiFrame 11.0. API організовано за функціональними областями для забезпечення чіткого розділення обов'язків та зручності використання.

## Базова URL-адреса
```
http://localhost:8000
```

## Автентифікація
Більшість ендпоінтів вимагають автентифікації. Використовуйте ендпоінт `/auth/login` для отримання токена сесії.

## Ендпоінти API

### Ендпоінти системи
- `GET /system/` - Кореневий ендпоінт
- `POST /system/mode/{mode}` - Встановити режим системи

### Ендпоінти автентифікації
- `POST /auth/login` - Вхід користувача
- `POST /auth/logout` - Вихід користувача

### Ендпоінти проектування мікросхем
- `POST /chip/process` - Створити процес мікросхеми
- `POST /chip/zero-defect` - Забезпечити проектування мікросхем без дефектів

### Ендпоінти аналітики
- `GET /analytics/metrics/{chip_id}` - Отримати метрики мікросхеми
- `GET /analytics/trends/{chip_id}` - Отримати тенденції мікросхеми

### Ендпоінти безпеки
- `GET /security/threats` - Отримати загрози безпеки

### Ендпоінти генерації хешів
- `POST /hash/rtl` - Генерувати RTL хеш

### Ендпоінти квантового моделювання
- `POST /simulate/quantum/{chip_id}` - Запустити квантове моделювання

### Ендпоінти співпраці
- `POST /chip/collaboration/` - Почати співпрацю
- `POST /chip/collaboration/update` - Оновити співпрацю

### Ендпоінти генерації драйверів
- `POST /chip/driver/` - Генерувати драйвер
- `POST /chip/driver/firmware/update` - Оновити прошивку

### Ендпоінти голосових команд
- `POST /voice/design` - Голосове проектування
- `POST /voice/quest` - Голосовий квест

### Ендпоінти інтерфейсу BCI
- `POST /bci/command` - Команда BCI

### Ендпоінти спільноти
- `POST /community/forum/create` - Створити форум
- `POST /community/post/add` - Додати повідомлення
- `POST /community/ip/share` - Поділитися IP-блоком
- `POST /community/chat` - Надіслати повідомлення в чат

### Ендпоінти мережі дизайнерів
- `POST /designer/register` - Зареєструвати дизайнера
- `POST /designer/connect` - Підключити дизайнера
- `POST /designer/rate` - Оцінити дизайнера

### Ендпоінти виробництва
- `GET /fab/analytics/{fab_name}` - Отримати аналітику виробництва

### Ендпоінти сервісів ШІ
- `GET /ai/trend/analyze/{chip_id}` - Аналіз тенденцій ШІ
- `GET /ai/strategy/predict` - Прогнозування стратегії ШІ

### Ендпоінти автоматичного масштабування
- `POST /auto/scale` - Автоматичне масштабування

### Ендпоінти VR-тренування
- `POST /vr/training/` - Почати VR-тренування

### Ендпоінти генерації IP-блоків
- `POST /ip/block/generate` - Генерувати IP-блок
- `POST /ip/block/publish` - Опублікувати IP-блок
- `POST /ip/block/purchase` - Придбати IP-блок
- `POST /ip/block/calculate` - Обчислити параметри IP-блоку

### Ендпоінти маркетплейсу
- `POST /marketplace/design/upload` - Завантажити проект
- `POST /marketplace/quantum/chip/design` - Проектування квантової мікросхеми
- `POST /marketplace/learning/quest/create` - Створити навчальний квест

### Ендпоінти голосування DAO
- `POST /dao/interactive/tour` - Інтерактивний тур

### Ендпоінти інтеграції Web3
- `POST /web3/nft/mint` - Створити NFT
- `POST /web3/nft/transfer` - Передати NFT

### Ендпоінти інтеграції IoT
- `POST /iot/connect` - Підключитися до IoT

### Ендпоінти захисту від загроз нульового дня
- `POST /zero/day/scan` - Сканувати на вразливості нульового дня
- `POST /zero/day/mitigate` - Усунути вразливості нульового дня

### Ендпоінти партнерської програми
- `POST /partner/register` - Зареєструвати партнера
- `POST /partner/government/subscription` - Державна підписка
- `POST /partner/government/order` - Державне замовлення

### Ендпоінти моніторингу тендерів
- `POST /tender/monitor` - Моніторити тендери

### Ендпоінти адміністративної панелі
- `POST /admin/config/update` - Оновити конфігурацію

### Ендпоінти перевірки здоров'я
- `GET /health/` - Перевірка здоров'я

## Ендпоінти WebSocket
- `WebSocket /ws/ar` - З'єднання WebSocket AR

## Відповіді про помилки
Всі ендпоінти повертають узгоджений формат відповідей про помилки:
```json
{
  "status": "error",
  "message": "Опис помилки"
}
```

## Відповіді про успіх
Більшість ендпоінтів повертають узгоджений формат відповідей про успіх:
```json
{
  "status": "success",
  "data": {}
}
```

## Обмеження швидкості
API реалізовує обмеження швидкості для запобігання зловживанням. Перевищення ліміту швидкості призведе до відповіді 429 Too Many Requests.

## Версіонування
Версія API вказана в шляху URL. Наразі доступна версія 1.0.0.

## Підтримка
Для отримання підтримки звертайтесь до команди GlobalScope MultiFrame.