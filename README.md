# IRIDA

Уеб базирана система за цялостно планиране, структуриране и управление на учебния процес в средни и професионални училища: специалности, учебни планове, предмети, раздели и теми с дидактически MoSCoW анализ, уроци/занятия (теория и практика), дидактически точки, бележки, задачи, прикачени файлове и вграден **AI асистент** за генериране на учебно съдържание и тематични разпределения.

Интерфейсът е реализиран чрез server-rendered Django шаблони (Bootstrap 5) и динамичен REST API (Django REST Framework), с който модулният JavaScript в `irida_app/frontend/irida/js/` управлява формите, таблиците и интерактивните диалогови прозорци.

---

## Структура на проекта

```
IRIDA/
├─ .env                      локални тайни и конфигурация (НЕ е в git)
├─ .env.example              шаблон за настройките в .env
├─ requirements/
│  ├─ base.txt               основни зависимости (Django, DRF, PyMySQL, Pillow и др.)
│  ├─ dev.txt                -r base.txt + debug-toolbar, stubs
│  └─ prod.txt               -r base.txt + whitenoise, gunicorn
└─ irida_app/                Django project root
   ├─ manage.py
   ├─ config/
   │  ├─ settings/
   │  │  ├─ base.py          общи настройки; чете променливите от .env
   │  │  ├─ dev.py           DEBUG=True, конзолна поща, локална среда
   │  │  └─ prod.py          DEBUG=False, сигурност (SECURE_*), логове
   │  ├─ urls.py
   │  ├─ wsgi.py
   │  └─ asgi.py
   ├─ main/                  основно приложение, разделено по домейни
   │  ├─ constants.py        номенклатури, роли, статуси и типове
   │  ├─ utils.py            помощни функции за изчисления и качване
   │  ├─ admin.py            Django Admin конфигурация
   │  ├─ urls.py             HTML маршрути и страници
   │  ├─ api_urls.py         REST API маршрути (префикс /api/)
   │  ├─ models/
   │  │  ├─ accounts.py      UserProfile, потребителски роли, Log
   │  │  ├─ attachments.py   SessionAttachment (файлове към уроци), AppAttachment
   │  │  ├─ curriculum.py    Subject (предмет), Unit (раздел), Topic (тема), Goal (цел)
   │  │  ├─ lessons.py       Session (урок/занятие), SessionTopic/Point/Note/Task
   │  │  ├─ prompts.py       AIPrompt (системни и потребителски AI шаблони)
   │  │  └─ schools.py       School (училище), Specialty (специалност), SchoolDayConfig
   │  ├─ serializers/        DRF сериализатори по домейни (curriculum, lessons, prompts, attachments...)
   │  ├─ views/
   │  │  ├─ auth.py          вход и изход на потребители
   │  │  ├─ pages.py         рендериране на HTML изгледи
   │  │  ├─ api_context.py   текущ потребителски контекст (училище, предмет, урок)
   │  │  ├─ api_curriculum.py операции с предмети, раздели, теми и цели
   │  │  ├─ api_lessons.py   управление на уроци, точки, задачи и бележки
   │  │  ├─ api_prompts.py   CRUD и филтриране на AI промптове
   │  │  ├─ api_attachments.py качване и управление на файлове към уроци
   │  │  ├─ api_schools.py   училища, специалности и конфигурация на учебен ден
   │  │  ├─ api_uploads.py   общо качване на медийни файлове
   │  │  └─ api_users.py     управление на профили и потребители
   │  ├─ tests.py            автоматизиран тестов пакет (43 теста)
   │  └─ migrations/         миграции на базата данни (0001 - 0044)
   ├─ templates/main/        Django шаблони
   │  └─ components/         преизползваеми компоненти (напр. ai_prompt_modal.html)
   ├─ frontend/              статични ресурси (source, следени в git)
   │  ├─ irida/              собствен JS/CSS код на приложението
   │  └─ css/  js/  libs/  images/  icon-fonts/
   ├─ static/                компилирана статика от collectstatic (НЕ е в git)
   └─ media/                 потребителски качени файлове (НЕ е в git)
```

---

## Стартиране в Development среда

### 1. Подготовка на виртуална среда и зависимости

```bash
python -m venv .venv

# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements/dev.txt
```

### 2. Конфигуриране на `.env`

Копирайте примерния файл и настройте параметрите за връзка с базата данни:

```bash
copy .env.example .env      # под Windows
# или
cp .env.example .env        # под Linux/macOS
```

Попълнете `DB_NAME`, `DB_USER`, `DB_PASSWORD` и `DJANGO_SECRET_KEY`.

### 3. Прилагане на миграции и стартиране

```bash
python irida_app/manage.py migrate
python irida_app/manage.py runserver
```

Приложението ще бъде достъпно на `http://127.0.0.1:8000/`.

---

## Автоматизирани тестове

Проектът разполага с цялостен тестов пакет в `irida_app/main/tests.py`, покриващ моделите, REST API endpoint-ите, правата за достъп, прикачването на файлове, AI промптовете и заместването на динамичните маркери.

За изпълнение на тестовете:

```bash
python irida_app/manage.py test main
```

---

## AI Помощник и генератор на промптове (AI Prompts)

Системата разполага с вграден модул за създаване, редактиране и използване на интелигентни AI промптове. Шаблоните се адаптират динамично спрямо текущия контекст на страницата чрез автоматично заместване на плейсхолдъри:

* `{предмет}` – Наименование на учебния предмет
* `{специалност}` – Наименование на специалността
* `{клас}` – Клас (8 – 12 клас)
* `{тема}` – Тема / заглавие на урок
* `{цели}` – Общи и специфични цели на обучението
* `{точки}` – План и дидактически точки на урока
* `{списък_уроци}` – Списък с въведените уроци и занятия
* `{раздели_и_теми}` – Структура на разделите и темите от учебната програма
* `{структура_часове}` – Хорариум и седмично разпределение по срокове

### Специфика при изчисляване на учебните срокове и седмици:
* **8, 9, 10 и 11 клас:** I срок – 18 учебни седмици; II срок – 18 учебни седмици (общо 36 седмици годишно).
* **12 клас:** I срок – 18 учебни седмици; II срок – 11 учебни седмици (общо 29 седмици годишно).

---

## Пускане в Production (cPanel / Passenger WSGI / SuperHosting)

### 1. Настройки на средата
В production режим се зарежда `config.settings.prod`:

```bash
export DJANGO_SETTINGS_MODULE=config.settings.prod
```

Задължителни променливи в `.env`:
* `DJANGO_SECRET_KEY` – сигурен таен ключ за криптографско подписване
* `DJANGO_ALLOWED_HOSTS` – списък с домейните на приложението (напр. `irida.example.com`)
* `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` – параметри за MySQL

### 2. Подготовка и стартиране
```bash
# Прилагане на миграциите:
python manage.py migrate

# Събиране на статичните файлове:
python manage.py collectstatic --noinput

# Проверка на конфигурацията преди пускане:
python manage.py check --deploy
```

### 3. Рестартиране на Passenger WSGI:
* През **cPanel -> Setup Python App -> Restart**
* Или през терминала в корена на приложението: `mkdir -p tmp && touch tmp/restart.txt`

---

## Лиценз и авторски права

Проектът е разработен за нуждите на средното професионално и общо образование. Всички права запазени.
