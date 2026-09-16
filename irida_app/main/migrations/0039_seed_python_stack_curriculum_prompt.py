from django.db import migrations

STACK_CURRICULUM_PROMPT = {
    'title': 'Анализ на учебна програма (МОН) и MoSCoW анализ (Python, Django, Vue.js, Bootstrap)',
    'page_key': 'course_units',
    'prompt_text': (
        'Действай като опитен методист и експерт по професионално образование и софтуерни технологии. '
        'Прикачвам официална учебна програма (утвърдена от МОН) за учебен предмет: "{предмет}" '
        '({клас} клас, специалност/професия: {специалност}).\n\n'
        '### 1. ТЕХНОЛОГИЧЕН СТЕК В УЧИЛИЩЕТО:\n'
        'Важно методическо уточнение за профила на обучението:\n'
        '- Основен език за програмиране: Python;\n'
        '- Основни библиотеки и frameworks: Django (Backend / Web API), Vue.js (CDN версия за реактивен Frontend), Axios.js (HTTP заявки и REST комуникация), Bootstrap 5 (потребителски интерфейс и стилове).\n\n'
        '### 2. МЕТОДИКА ЗА АНАЛИЗ И ПРИОРИТИЗАЦИЯ (MoSCoW):\n'
        'Моля, анализирай учебното съдържание от приложения документ и направи детайлен MoSCoW (MSCW) анализ, '
        'като стриктно съобразиш приоритизацията с изучавания технологичен стек (Python, Django, Vue.js, Axios, Bootstrap) по следната методика:\n'
        '1. Извлечи всички раздели от програмата и посочи минималния им препоръчителен брой учебни часове (hours).\n'
        '2. За всеки раздел извлечи конкретните теми (topics) и определи за всяка тема нейната категория по MoSCoW, отчитайки избрания стек:\n'
        '   - "M" (Must / Задължителна) – Фундаментални концепции, базови синтактични основи и критични принципи, покриващи ДОС и директно приложими в стека Python / Django / Vue / Bootstrap;\n'
        '   - "S" (Should / Важна) – Важни теми, архитектурни модели и добри практики за практическо задълбочаване с Python, Django, Vue.js и REST интеграция;\n'
        '   - "C" (Could / Пожелателна) – Обогатяващи теми за напреднали ученици, допълнителни библиотеки, усъвършенствани компоненти и разширения;\n'
        '   - "W" (Won\'t / Отпадаща) – Тясно специализирани, несъвместими с избрания стек (напр. чужди за стека езици/технологии или остарели библиотеки) или детайли, които не са приоритет за този курс.\n'
        '3. За всяка тема посочи кратка и точна педагогическа обосновка (MoSCoW_rem) за избора на съответната категория, отразяваща връзката с изучавания технологичен стек.\n\n'
        '### 3. ФОРМАТ НА ИЗХОДА:\n'
        'Върни резултата ЕДИНСТВЕНО като валиден JSON масив (без излишен съпътстващ свободен текст), готов за директен импорт в приложението ИРИДА:\n'
        '[\n'
        '  {\n'
        '    "num": 1,\n'
        '    "name": "Име на раздел 1",\n'
        '    "hours": 10,\n'
        '    "topics": [\n'
        '      {\n'
        '        "num": 1,\n'
        '        "name": "Име на тема 1.1",\n'
        '        "MoSCoW_cat": "M",\n'
        '        "MoSCoW_rem": "Основни концепции и базисен синтаксис в Python"\n'
        '      },\n'
        '      {\n'
        '        "num": 2,\n'
        '        "name": "Име на тема 1.2",\n'
        '        "MoSCoW_cat": "S",\n'
        '        "MoSCoW_rem": "Практическо приложение и интеграция с Django / Vue"\n'
        '      }\n'
        '    ]\n'
        '  }\n'
        ']'
    ),
    'instructions': (
        '1. Копирайте промпта;\n'
        '2. Отворете външния си AI инструмент (ChatGPT, Claude, Gemini, DeepSeek и др.);\n'
        '3. Прикачете файла с учебната програма (DOCX/PDF от МОН);\n'
        '4. Поставете промпта и изпратете съобщението;\n'
        '5. Копирайте генерирания JSON код;\n'
        '6. Натиснете бутона „Импорт на програма“ до „Добави раздел“ на тази страница и поставете JSON кода (или качете записания файл) за автоматично зареждане.'
    ),
    'is_system': True,
    'order': 3,
}


def seed_stack_curriculum_prompt(apps, schema_editor):
    AIPrompt = apps.get_model('main', 'AIPrompt')
    prompt = AIPrompt.objects.filter(
        page_key=STACK_CURRICULUM_PROMPT['page_key'],
        title=STACK_CURRICULUM_PROMPT['title'],
        is_system=True
    ).first()
    if prompt:
        prompt.prompt_text = STACK_CURRICULUM_PROMPT['prompt_text']
        prompt.instructions = STACK_CURRICULUM_PROMPT['instructions']
        prompt.order = STACK_CURRICULUM_PROMPT['order']
        prompt.save()
    else:
        AIPrompt.objects.create(**STACK_CURRICULUM_PROMPT)


def unseed_stack_curriculum_prompt(apps, schema_editor):
    AIPrompt = apps.get_model('main', 'AIPrompt')
    AIPrompt.objects.filter(
        title=STACK_CURRICULUM_PROMPT['title'],
        page_key=STACK_CURRICULUM_PROMPT['page_key'],
        is_system=True
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0038_seed_topic_distribution_template_prompts'),
    ]

    operations = [
        migrations.RunPython(seed_stack_curriculum_prompt, unseed_stack_curriculum_prompt),
    ]
