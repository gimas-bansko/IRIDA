from django.db import migrations

IMPORT_PROMPT = {
    'title': 'Анализ на учебна програма (МОН) и генериране на раздели и теми с MoSCoW анализ',
    'page_key': 'course_units',
    'prompt_text': (
        'Действай като опитен методист и експерт по професионално образование. '
        'Прикачвам официална учебна програма (утвърдена от МОН) за учебен предмет: "{предмет}" '
        '({клас} клас, специалност/професия: {специалност}).\n\n'
        'Моля, анализирай учебното съдържание от приложения документ и направи детайлен MoSCoW (MSCW) анализ по следната методика:\n'
        '1. Извлечи всички раздели от програмата и посочи минималния им препоръчителен брой учебни часове (hours).\n'
        '2. За всеки раздел извлечи конкретните теми (topics) и определи за всяка тема нейната категория по MoSCoW:\n'
        '   - "M" (Must / Задължителна) – Фундаментални концепции, базови синтактични основи и критични принципи, покриващи ДОС;\n'
        '   - "S" (Should / Важна) – Важни теми и добри практики за практическо задълбочаване;\n'
        '   - "C" (Could / Пожелателна) – Обогатяващи теми за напреднали ученици и разширения;\n'
        '   - "W" (Won\'t / Отпадаща) – Тясно специализирани или остарели детайли, които не са приоритет за този курс.\n'
        '3. За всяка тема посочи кратка и точна педагогическа обосновка (MoSCoW_rem) за избора на съответната категория.\n\n'
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
        '        "MoSCoW_rem": "Основни концепции и базисен синтаксис"\n'
        '      },\n'
        '      {\n'
        '        "num": 2,\n'
        '        "name": "Име на тема 1.2",\n'
        '        "MoSCoW_cat": "S",\n'
        '        "MoSCoW_rem": "Практическо приложение и упражнение"\n'
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
    'order': 2,
}


def seed_import_prompt(apps, schema_editor):
    AIPrompt = apps.get_model('main', 'AIPrompt')
    AIPrompt.objects.get_or_create(
        title=IMPORT_PROMPT['title'],
        page_key=IMPORT_PROMPT['page_key'],
        defaults=IMPORT_PROMPT
    )


def unseed_import_prompt(apps, schema_editor):
    AIPrompt = apps.get_model('main', 'AIPrompt')
    AIPrompt.objects.filter(
        title=IMPORT_PROMPT['title'],
        page_key=IMPORT_PROMPT['page_key'],
        is_system=True
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_seed_ai_prompts'),
    ]

    operations = [
        migrations.RunPython(seed_import_prompt, unseed_import_prompt),
    ]
