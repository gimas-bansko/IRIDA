# Типове въпроси

TYPE1 = 1
TYPE2 = 2
TYPE3 = 3
TYPE4 = 4
TYPE5 = 5
TASK_TYPE = [
    (TYPE1, 'затворен тип без картинка'),
    (TYPE2, 'затворен тип с картинка'),
    (TYPE3, 'съпоставяне ляво --> дясно'),
    (TYPE4, 'съпоставяне картинка --> опции'),
    (TYPE5, 'отворен отговор'),
]

# Нива по Блум
LEVEL1 = 1
LEVEL2 = 2
LEVEL3 = 3
LEVEL4 = 4
LEVEL_TYPE = [
    (LEVEL1, 'знание'),
    (LEVEL2, 'разбиране'),
    (LEVEL3, 'приложение'),
    (LEVEL4, 'анализ'),
]

# Теми за визията на интерфейса
DARK = 1
LIGHT = 2
THEME_TYPE = [
    (DARK, 'тъмна'),
    (LIGHT, 'светла'),
]

# Роли
SUPERADMIN= 1
GUESTADMIN = 2
SCHOOLADMIN = 3
TEACHER = 4
STUDENT = 5

USER_LEVEL = [
    (SUPERADMIN, 'Системен администратор'),
    (GUESTADMIN, 'НАБЛЮДАВАЩ АДМИНИСТРАТОР'),
    (SCHOOLADMIN, 'УЧИЛИЩЕН АДМИНИСТРАТОР'),
    (TEACHER, 'УЧИТЕЛ'),
    (STUDENT, 'УЧЕНИК'),
]

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        return context

def update_test_statistics(test_result, answers):
    """
    Актуализира статистиките за теста и въпросите.
    """
    total_difficulty = 0
    for answer in answers:
        # Актуализиране на статистиките за въпроса
        answer.task.update_statistics(answer.is_correct, answer.points)
        total_difficulty += answer.task.level

    # Актуализиране на средната трудност на теста
    test_result.average_difficulty = total_difficulty / len(answers)
    test_result.save()


