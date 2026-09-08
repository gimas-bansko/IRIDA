# IRIDA

Django приложение за планиране на учебни програми и уроци: специалности,
учебни предмети, раздели и теми, уроци с точки от плана, бележки и задачи.

Интерфейсът е server-rendered (Django templates) + REST API (DRF), който
JavaScript-ът в `irida_app/frontend/irida/js/` ползва за таблиците и формите.

## Структура

```
IRIDA/
├─ .env                      локални тайни - НЕ е в git
├─ .env.example              шаблон за .env
├─ requirements/
│  ├─ base.txt               общи зависимости
│  ├─ dev.txt                -r base.txt + type stubs, debug-toolbar
│  └─ prod.txt               -r base.txt + whitenoise, gunicorn
└─ irida_app/                Django project root
   ├─ manage.py
   ├─ config/
   │  ├─ settings/
   │  │  ├─ base.py          общо; чете тайните от обкръжението
   │  │  ├─ dev.py           DEBUG=True, debug-toolbar, конзолна поща
   │  │  └─ prod.py          DEBUG=False, SECURE_*, whitenoise, логове
   │  ├─ urls.py
   │  ├─ wsgi.py
   │  └─ asgi.py
   ├─ main/                  единствено приложение, разделено по домейни
   │  ├─ constants.py        номенклатури (роли, теми, choices)
   │  ├─ utils.py            помощни функции
   │  ├─ admin.py
   │  ├─ urls.py             HTML маршрути
   │  ├─ api_urls.py         API маршрути (префикс api/)
   │  ├─ models/
   │  │  ├─ curriculum.py    Subject, Unit, Topic, Goal
   │  │  ├─ lessons.py       Session, SessionTopic/Point/Note/Task
   │  │  ├─ schools.py       Specialty, School, Documents
   │  │  └─ accounts.py      UserProfile, Log + сигнали
   │  ├─ serializers/        същото разделение по домейни
   │  ├─ views/
   │  │  ├─ auth.py          вход/изход
   │  │  ├─ pages.py         HTML страници
   │  │  ├─ api_context.py   контекст на потребителя
   │  │  ├─ api_schools.py
   │  │  ├─ api_curriculum.py
   │  │  ├─ api_lessons.py
   │  │  ├─ api_uploads.py
   │  │  └─ api_users.py
   │  └─ migrations/
   ├─ templates/main/        шаблони (ниво проект)
   ├─ frontend/              статика - source, в git
   │  ├─ irida/              собствен код на IRIDA (js, images)
   │  ├─ css/  js/  libs/  sass/  images/  icon-fonts/
   │  └─ css_admin/          алтернативна тема, НЕ се ползва (виж по-долу)
   ├─ static/                изход на collectstatic - НЕ е в git
   └─ media/                 качени файлове - НЕ е в git
```

Всички модели са в един Django app (`main`), затова разделянето на модули
не променя имената на таблиците (`main_subject`, `main_session`, ...) и не
изисква нови миграции.

## Стартиране

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements/dev.txt

copy .env.example .env      # после попълни DB_PASSWORD и DJANGO_SECRET_KEY

python irida_app\manage.py migrate
python irida_app\manage.py runserver
```

`manage.py`, `wsgi.py` и `asgi.py` ползват `config.settings.dev` по подразбиране.

## Production

Настройките се избират през обкръжението:

```bash
set DJANGO_SETTINGS_MODULE=config.settings.prod
```

`prod.py` изисква следните променливи и **отказва да стартира без тях** -
нарочно, за да не тръгне приложението с несигурни стойности:

| Променлива | За какво е |
|---|---|
| `DJANGO_SECRET_KEY` | подписване на сесии и токени |
| `DJANGO_ALLOWED_HOSTS` | домейни, от които се приемат заявки |
| `DB_PASSWORD` | парола за MySQL |

Преди пускане:

```bash
python irida_app\manage.py check --deploy
python irida_app\manage.py collectstatic
```

`SECURE_HSTS_SECONDS` е 3600 по подразбиране. Вдигни го само след като си
сигурен, че HTTPS работи навсякъде - иначе рискуваш да си заключиш домейна.

## Известни проблеми

Неща, намерени при рефакторинга и **още неоправени**. Подредени по важност.

### 1. Паролата за MySQL е била в git историята

`irida_app/settings.py` съдържаше `PASSWORD: '1613'` в коммитнат вид.
Изваждането ѝ в `.env` не я маха от историята. Смени я реално:

```sql
ALTER USER 'gimas'@'localhost' IDENTIFIED BY '<нова парола>';
```

и обнови `DB_PASSWORD` в `.env`.

`SECRET_KEY` вече е сменен - старите сесии са невалидни, нужно е ново логване.

### 2. Немигрирани промени по моделите

`makemigrations` показва 7 чакащи промени по `Session` и `SessionTopic`.
Този дрейф е **от преди** рефакторинга (проверено срещу `HEAD:models.py`) -
модели са редактирани без `makemigrations`. Промените са само метаданни
(`verbose_name`, `help_text`, `choices`, `ordering`, `validators`), няма
схемни промени. Направи бекъп и пусни:

```bash
python irida_app\manage.py makemigrations main
python irida_app\manage.py migrate
```

### 3. Два бъга в задаването на предмет по подразбиране

`views/api_context.py`. Запазени умишлено, за да не смесвам поправки
с преструктурирането:

- `set_subject()` при POST присвоява на `sp` вместо на `sb`, тоест
  POST без `sb` в URL не сменя нищо.
- `set_course()` при POST чете ключ `'sp'` вместо `'sb'`.

### 4. `make_user_context()` пада при потребител без училище

`views/pages.py` вика `user_profile.school.specialities.all()`, а
`UserProfile.school` е `null=True`. Всеки потребител без зададено училище
получава `AttributeError` (500) на всяка страница.

### 5. `USER_LEVEL[access_level - 1][1]` е чуплив

На три места ролята се чете по индекс в списъка вместо през
`user_profile.get_access_level_display()`. Разчита на това, че `USER_LEVEL`
е подреден и започва от 1.

### 6. `@csrf_exempt` върху DRF endpoint-и

`api_lessons.py` и `api_uploads.py` имат `@csrf_exempt` под `@api_view`.
Почти сигурно е без ефект (DRF прилага `csrf_exempt` сама на външния view,
а `SessionAuthentication` налага CSRF отделно), но не е проверено с
реална заявка. Оставено както е било; маркирано с коментари.

### 7. Мъртъв код

Запазен, защото описва замисъл, а не защото се ползва:

| Къде | Какво |
|---|---|
| `constants.py` | `TASK_TYPE`, `LEVEL_TYPE` - планиран модул за тестове |
| `utils.py` | `update_test_statistics()` - разчита на несъществуващ модел `Task` |
| `utils.py` | `session_image_upload_path()` - би оправил презаписването на файлове с еднакви имена |
| `admin.py` | `SpecialtyFilter` - филтрира по `theme_id`, поле, което не съществува |
| `serializers/schools.py` | `SchoolSerializer2`, `SchoolLogoSerializer` |
| `views/auth.py` | `sign_in()` |
| `views/pages.py` | `session_main_view_old()` - маршрутът `session_main_old` сочи към `session_main_view` |
| `templates/main/` | `session_main_old.html` + базата му `session_main_base.html` |
| `frontend/css_admin/` | 13 MB алтернативна тема, нула референции |

`SessionTopicReadSerializer` и `SessionTopicReadSerializerDetailed` са
идентични - вторият се пази само защото `SessionTopicsForSessionView`
го ползва по това име.

### 8. Няма тестове

`main/tests.py` е празен.
