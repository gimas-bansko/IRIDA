from django.db import migrations


def fix_grade_12_term_weeks(apps, schema_editor):
    AIPrompt = apps.get_model('main', 'AIPrompt')
    for prompt in AIPrompt.objects.all():
        changed = False
        text = prompt.prompt_text
        if '12 учебни седмици (за 12 клас)' in text:
            text = text.replace('12 учебни седмици (за 12 клас)', '11 учебни седмици (за 12 клас)')
            changed = True
        if '12 седмици (12 клас)' in text:
            text = text.replace('12 седмици (12 клас)', '11 седмици (12 клас)')
            changed = True
        if 'от 1 до 30 за 12 клас' in text:
            text = text.replace('от 1 до 30 за 12 клас', 'от 1 до 29 за 12 клас')
            changed = True
        if changed:
            prompt.prompt_text = text
            prompt.save()


def rollback_fix_grade_12_term_weeks(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0042_update_topic_distribution_template_prompts'),
    ]

    operations = [
        migrations.RunPython(fix_grade_12_term_weeks, rollback_fix_grade_12_term_weeks),
    ]
