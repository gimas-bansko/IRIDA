---
sessionId: session-260921-222955-17o9
---

# Requirements

### Overview & Goals
Целта е безопасно и цялостно пренасяне на новите функционалности за прикачени файлове (маркери за системност/авторство, филтриране и права за достъп) от локалната среда към Linux хостинг в SuperHosting.bg (cPanel с Phusion Passenger WSGI).

### Scope
#### In Scope
- Качване на новата миграция `0045_appattachment_created_by_appattachment_is_system.py`.
- Обновяване на бекенд кода (`models`, `serializers`, `views`, `admin`).
- Обновяване на фронтенд темплейта (`attachments.html`) и клиентския скрипт (`attachments.js`).
- Изпълнение на миграциите върху MySQL базата на хостинга.
- Синхронизиране на статичните файлове чрез `collectstatic`.
- Рестартиране на Passenger WSGI процеса.

#### Out of Scope
- Преконфигуриране на базовите настройки на виртуалната среда или домейна.
- Промени по конфигурацията на базата данни в `.env`.

# Technical Design

### Current Implementation
Промените включват:
- **Модели и миграции:** `irida_app/main/models/attachments.py`, `irida_app/main/migrations/0045_appattachment_created_by_appattachment_is_system.py`
- **API и сериализатори:** `irida_app/main/serializers/attachments.py`, `irida_app/main/views/api_attachments.py`
- **UI и шаблони:** `irida_app/templates/main/attachments.html`, `irida_app/frontend/irida/js/attachments.js`
- **Администрация:** `irida_app/main/admin.py`

### Deployment Architecture & Workflow
1. **Source Control:** Локалните промени се избутват към Git (GitHub / GitLab / Bitbucket).
2. **Hosting Environment:** Влизане през SSH или cPanel Terminal -> `git pull`.
3. **Database Migration:** Изпълнение на `manage.py migrate` през активната Python виртуална среда.
4. **Static Compilation:** Изпълнение на `manage.py collectstatic --noinput` за запис на новия `attachments.js` в `static/`.
5. **Passenger WSGI Reload:** Извикване на рестарт през `cPanel -> Setup Python App -> Restart` или чрез обнов��ване на маркера `tmp/restart.txt`.

### Key Commands Reference
```bash
# На хостинга (след активиране на virtualenv):
cd irida_app
python manage.py migrate
python manage.py collectstatic --noinput
mkdir -p tmp && touch tmp/restart.txt
```

# Delivery Steps

### ✓ Step 1: Commit and push changes to repository
Подготовка на локалните промени и качването им в отдалеченото хранилище.

- Добавяне и потвърждаване на новия миграционен файл `irida_app/main/migrations/0045_appattachment_created_by_appattachment_is_system.py`.
- Добавяне на променените Python файлове (`attachments.py`, `api_attachments.py`, `admin.py`, `tests.py`).
- Добавяне на променените темплейти и JavaScript файлове (`attachments.html`, `attachments.js`).
- Изпълнение на `git commit` и `git push origin master`.

###   Step 2: Pull updates and run database migrations on hosting
Актуализиране на кода на сървъра и прилагане на миграциите към базата данни.

- Изтегляне на новите промени в хостинг директорията чрез `git pull origin master` през SSH/cPanel Terminal.
- Активиране на Python виртуалната среда (`source .../bin/activate`).
- Изпълнение на `python manage.py migrate` за създаване на полетата `is_system` и `created_by_id` в таблицата `main_appattachment`.

###   Step 3: Collect static assets and restart Passenger WSGI
Сглобяване на статичните файлове и рестартиране на WSGI процеса за отразяване на новите функционалности.

- Изпълнение на `python manage.py collectstatic --noinput` за обновяване на статичните JS и CSS ресурси.
- Рестартиране на Passenger WSGI чрез cPanel (Setup Python App -> Restart) или чрез `touch tmp/restart.txt`.
- Валидация на страницата `/attachments/` в браузъра с изчистване на браузърния кеш.