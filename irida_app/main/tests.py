import re
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from main.constants import STUDENT, TEACHER
from main.models import (
    AIPrompt,
    AppAttachment,
    Goal,
    School,
    SchoolDayConfig,
    Session,
    SessionAttachment,
    SessionNote,
    SessionPoint,
    SessionTask,
    SessionTopic,
    Specialty,
    Subject,
    Topic,
    Unit,
    UserProfile,
)


class TopicModelTest(TestCase):
    def setUp(self):
        self.school = School.objects.create(full_name='Тестово училище', short_name='ТУ', city='София')
        self.specialty = Specialty.objects.create(school=self.school, specialty_name='Информатика')
        self.subject = Subject.objects.create(specialty=self.specialty, name='Програмиране', grade=10)
        self.unit = Unit.objects.create(subject=self.subject, num=1, name='Раздел 1', hours=10)

    def test_topic_moscow_rem_long_text(self):
        long_rem = "А" * 500
        topic = Topic.objects.create(
            unit=self.unit,
            num=1,
            name='Тема 1',
            MoSCoW_cat='M',
            MoSCoW_rem=long_rem
        )
        self.assertEqual(len(topic.MoSCoW_rem), 500)
        self.assertEqual(topic.MoSCoW_rem, long_rem)


class SessionAttachmentAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)
        self.school = School.objects.create(full_name='Тестово училище', short_name='ТУ', city='София')
        self.specialty = Specialty.objects.create(school=self.school, specialty_name='Информатика')
        self.subject = Subject.objects.create(specialty=self.specialty, name='Програмиране', grade=10)
        self.session = Session.objects.create(course=self.subject, num=1, name='Уводно занятие')
        self.point = SessionPoint.objects.create(session=self.session, num=1, name='Точка 1', duration=15)

    def test_create_and_list_attachment(self):
        # 1. Create theory attachment via upsert with file
        test_file = SimpleUploadedFile("theory_doc.pdf", b"PDF file content", content_type="application/pdf")
        create_data = {
            'id': 0,
            'session': self.session.id,
            'point': self.point.id,
            'num': 1,
            'name': 'Теория 1',
            'attachment_type': 'theory',
            'description': 'Описание на теорията',
            'file': test_file
        }
        resp = self.client.post('/api/session-attachments/upsert/', create_data, format='multipart')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        theory_id = resp.data['id']
        self.assertEqual(resp.data['name'], 'Теория 1')
        self.assertEqual(resp.data['attachment_type'], 'theory')
        self.assertEqual(resp.data['description'], 'Описание на теорията')
        self.assertTrue(resp.data['file_url'].endswith('.pdf'))
        self.assertTrue(resp.data['file_url'].startswith('/media/session_attachments/'))
        self.assertTrue(resp.data['file_name'].endswith('.pdf'))

        # Create other attachment via upsert
        other_file = SimpleUploadedFile("appendix.zip", b"ZIP content", content_type="application/zip")
        other_data = {
            'id': 0,
            'session': self.session.id,
            'point': '',
            'num': 1,
            'name': 'Приложение 1',
            'attachment_type': 'other',
            'description': 'Архив с код',
            'file': other_file
        }
        resp_other = self.client.post('/api/session-attachments/upsert/', other_data, format='multipart')
        self.assertEqual(resp_other.status_code, status.HTTP_201_CREATED)
        other_id = resp_other.data['id']
        self.assertEqual(resp_other.data['attachment_type'], 'other')

        # 2. List all attachments for session
        list_resp = self.client.get(f'/api/sessions/{self.session.id}/attachments/')
        self.assertEqual(list_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_resp.data), 2)

        # 3. List filtered attachments
        theory_list = self.client.get(f'/api/sessions/{self.session.id}/attachments/?type=theory')
        self.assertEqual(len(theory_list.data), 1)
        self.assertEqual(theory_list.data[0]['id'], theory_id)

        other_list = self.client.get(f'/api/sessions/{self.session.id}/attachments/?type=other')
        self.assertEqual(len(other_list.data), 1)
        self.assertEqual(other_list.data[0]['id'], other_id)

        # 4. Update attachment via upsert (keeping existing file)
        update_data = {
            'id': theory_id,
            'session': self.session.id,
            'point': '',
            'num': 1,
            'name': 'Теория 1 Редактирано',
            'attachment_type': 'theory',
            'description': 'Ново описание'
        }
        update_resp = self.client.post('/api/session-attachments/upsert/', update_data, format='multipart')
        self.assertEqual(update_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(update_resp.data['name'], 'Теория 1 Редактирано')
        self.assertEqual(update_resp.data['description'], 'Ново описание')
        self.assertIsNotNone(update_resp.data['file_url'])

        # 5. Delete attachment
        del_resp = self.client.delete(f'/api/session-attachments/{theory_id}/')
        self.assertEqual(del_resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SessionAttachment.objects.count(), 1)


class SchoolDayConfigAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testadmin', password='password123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_default_config(self):
        response = self.client.get('/api/school-day-config/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['school_day_start'], '08:00')
        self.assertEqual(response.data['school_lessons_count'], 7)
        self.assertEqual(response.data['lesson_duration_minutes'], 45)
        self.assertEqual(response.data['first_break_duration_minutes'], 20)
        self.assertEqual(response.data['regular_break_duration_minutes'], 10)

    def test_update_config(self):
        update_data = {
            'school_day_start': '08:30',
            'school_lessons_count': 6,
            'lesson_duration_minutes': 40,
            'first_break_duration_minutes': 25,
            'regular_break_duration_minutes': 15,
        }
        response = self.client.put('/api/school-day-config/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['school_day_start'], '08:30')
        self.assertEqual(response.data['school_lessons_count'], 6)
        self.assertEqual(response.data['lesson_duration_minutes'], 40)
        self.assertEqual(response.data['first_break_duration_minutes'], 25)
        self.assertEqual(response.data['regular_break_duration_minutes'], 15)

        config = SchoolDayConfig.get_config()
        self.assertEqual(config.school_day_start, '08:30')
        self.assertEqual(config.school_lessons_count, 6)


class StudentPortalTest(TestCase):
    def setUp(self):
        self.school = School.objects.create(full_name='Училище 1', short_name='У1', city='София')
        self.specialty = Specialty.objects.create(school=self.school, specialty_name='Софтуерно инженерство')
        self.subject = Subject.objects.create(specialty=self.specialty, name='Обектно-ориентирано програмиране', grade=10)
        self.session = Session.objects.create(course=self.subject, num=1, name='Класове и обекти')
        self.task = SessionTask.objects.create(session=self.session, num=1, name='Задача 1', condition='Условие', answer='Отговор')
        self.attachment = SessionAttachment.objects.create(session=self.session, num=1, name='Теория 1', attachment_type='theory')

        # Create student user
        self.student_user = User.objects.create_user(username='student1', password='password123', first_name='Иван', last_name='Иванов')
        self.student_profile = self.student_user.userprofile
        self.student_profile.access_level = STUDENT
        self.student_profile.school = self.school
        self.student_profile.speciality = self.specialty
        self.student_profile.subject = self.subject
        self.student_profile.grade = 10
        self.student_profile.section = 'а'
        self.student_profile.save()

        # Create teacher user
        self.teacher_user = User.objects.create_user(username='teacher1', password='password123', first_name='Петър', last_name='Петров')
        self.teacher_profile = self.teacher_user.userprofile
        self.teacher_profile.access_level = TEACHER
        self.teacher_profile.school = self.school
        self.teacher_profile.speciality = self.specialty
        self.teacher_profile.subject = self.subject
        self.teacher_profile.grade = 10
        self.teacher_profile.section = 'а'
        self.teacher_profile.save()

    def test_student_login_redirect(self):
        client = Client()
        resp = client.post('/login', {'username': 'student1', 'password': 'password123'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/student_lessons')

    def test_teacher_login_redirect(self):
        client = Client()
        resp = client.post('/login', {'username': 'teacher1', 'password': 'password123'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/home')

    def test_student_lessons_page_access(self):
        client = Client()
        client.login(username='student1', password='password123')
        resp = client.get('/student_lessons')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'ИРИДА - Уроци за ученика')

    def test_student_welcome_redirect(self):
        client = Client()
        client.login(username='student1', password='password123')
        resp = client.get('/home')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/student_lessons')

    def test_subject_sessions_with_topics_api(self):
        client = APIClient()
        client.force_authenticate(user=self.student_user)
        resp = client.get(f'/api/subjects/{self.subject.id}/sessions-with-topics/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)
        session_data = resp.data[0]
        self.assertEqual(len(session_data['session_tasks']), 1)
        self.assertEqual(session_data['session_tasks'][0]['name'], 'Задача 1')
        self.assertEqual(len(session_data['session_attachments']), 1)
        self.assertEqual(session_data['session_attachments'][0]['attachment_type'], 'theory')


class AIPromptAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.teacher_user = User.objects.create_user(username='teacher_ai', password='password123', first_name='Иван', last_name='Иванов')
        self.admin_user = User.objects.create_superuser(username='admin_ai', password='password123', email='admin@test.com')
        self.client.force_authenticate(user=self.teacher_user)

    def test_list_prompts_with_page_key(self):
        # Create sample prompt
        AIPrompt.objects.create(
            title='Тест промпт за урок',
            page_key='lesson_main',
            prompt_text='План за {тема}',
            instructions='Указания',
            is_system=False,
            created_by=self.teacher_user
        )
        resp = self.client.get('/api/prompts/?page_key=lesson_main')
        self.assertEqual(resp.status_code, 200)
        # Should include lesson_main prompts and general prompts
        keys = {p['page_key'] for p in resp.data}
        self.assertTrue(keys.issubset({'lesson_main', 'general'}))
        self.assertTrue(any(p['title'] == 'Тест промпт за урок' for p in resp.data))

    def test_create_and_update_prompt(self):
        # Create
        resp = self.client.post('/api/prompts/upsert/', {
            'id': 0,
            'title': 'Мой нов промпт',
            'page_key': 'lesson_main',
            'prompt_text': 'Текст на промпта с {тема}',
            'instructions': 'Някакви указания',
            'order': 5
        }, format='json')
        self.assertEqual(resp.status_code, 201)
        created_id = resp.data['id']
        self.assertEqual(resp.data['title'], 'Мой нов промпт')
        self.assertEqual(resp.data['created_by_name'], 'Иван Иванов')

        # Update
        resp_update = self.client.post('/api/prompts/upsert/', {
            'id': created_id,
            'title': 'Мой обновен промпт',
            'page_key': 'lesson_main',
            'prompt_text': 'Обновен текст',
            'instructions': 'Нови указания',
            'order': 3
        }, format='json')
        self.assertEqual(resp_update.status_code, 200)
        self.assertEqual(resp_update.data['title'], 'Мой обновен промпт')

    def test_delete_user_prompt(self):
        prompt = AIPrompt.objects.create(
            title='За изтриване',
            page_key='lesson_main',
            prompt_text='Текст',
            is_system=False,
            created_by=self.teacher_user
        )
        resp = self.client.delete(f'/api/prompts/{prompt.id}/')
        self.assertEqual(resp.status_code, 204)
        self.assertFalse(AIPrompt.objects.filter(id=prompt.id).exists())

    def test_system_prompt_protection_for_normal_teacher(self):
        sys_prompt = AIPrompt.objects.create(
            title='Системен промпт',
            page_key='general',
            prompt_text='Системен текст',
            is_system=True
        )
        # Teacher tries to delete system prompt -> 403
        resp = self.client.delete(f'/api/prompts/{sys_prompt.id}/')
        self.assertEqual(resp.status_code, 403)

        # Teacher tries to edit system prompt -> 403
        resp_edit = self.client.post('/api/prompts/upsert/', {
            'id': sys_prompt.id,
            'title': 'Опит за редакция',
            'page_key': 'general',
            'prompt_text': 'Нов текст',
        }, format='json')
        self.assertEqual(resp_edit.status_code, 403)


class CurriculumImportAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='teacher_curriculum', password='password123')
        self.client.force_authenticate(user=self.user)
        self.subject = Subject.objects.create(name='Обектно-ориентирано програмиране', grade=11, subject_type='теория', hpy=72)

    def test_import_curriculum_replace_mode(self):
        # Initial unit
        old_unit = Unit.objects.create(subject=self.subject, num=1, name='Стар раздел', hours=4)
        Topic.objects.create(unit=old_unit, num=1, name='Стара тема', MoSCoW_cat='M')

        payload = {
            'units': [
                {
                    'num': 1,
                    'name': 'Раздел 1: Класове и обекти',
                    'hours': 10,
                    'topics': [
                        {'num': 1, 'name': 'Дефиниране на класове', 'MoSCoW_cat': 'M', 'MoSCoW_rem': 'Базов синтаксис'},
                        {'num': 2, 'name': 'Конструктори и деструктори', 'MoSCoW_cat': 'S', 'MoSCoW_rem': 'Важно за инициализация'},
                    ]
                },
                {
                    'num': 2,
                    'name': 'Раздел 2: Наследяване и полиморфизъм',
                    'hours': 14,
                    'topics': [
                        {'num': 1, 'name': 'Базови и производни класове', 'MoSCoW_cat': 'M', 'MoSCoW_rem': 'Основа на ООП'},
                    ]
                }
            ],
            'replace_existing': True
        }

        resp = self.client.post(f'/api/subjects/{self.subject.id}/import-curriculum/', payload, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data['units']), 2)

        # Database verification
        units = Unit.objects.filter(subject=self.subject).order_by('num')
        self.assertEqual(units.count(), 2)
        self.assertEqual(units[0].name, 'Раздел 1: Класове и обекти')
        self.assertEqual(units[0].unit_topic.count(), 2)
        self.assertEqual(units[1].name, 'Раздел 2: Наследяване и полиморфизъм')
        self.assertEqual(units[1].unit_topic.count(), 1)
        self.assertFalse(Unit.objects.filter(name='Стар раздел').exists())

    def test_import_curriculum_append_mode(self):
        Unit.objects.create(subject=self.subject, num=1, name='Съществуващ раздел 1', hours=6)

        payload = {
            'units': [
                {
                    'num': 1,
                    'name': 'Нов добавен раздел',
                    'hours': 8,
                    'topics': [
                        {'num': 1, 'name': 'Нова тема', 'MoSCoW_cat': 'C', 'MoSCoW_rem': 'За напреднали'}
                    ]
                }
            ],
            'replace_existing': False
        }

        resp = self.client.post(f'/api/subjects/{self.subject.id}/import-curriculum/', payload, format='json')
        self.assertEqual(resp.status_code, 200)

        # Both units must exist, with distinct numbers
        units = Unit.objects.filter(subject=self.subject).order_by('num')
        self.assertEqual(units.count(), 2)
        self.assertEqual(units[0].name, 'Съществуващ раздел 1')
        self.assertEqual(units[1].name, 'Нов добавен раздел')
        self.assertEqual(units[1].num, 2)

    def test_import_curriculum_linked_session_protection(self):
        unit = Unit.objects.create(subject=self.subject, num=1, name='Раздел със занятие', hours=4)
        topic = Topic.objects.create(unit=unit, num=1, name='Тема със занятие', MoSCoW_cat='M')
        from .models import Session, SessionTopic
        session = Session.objects.create(course=self.subject, num=1, name='Урок 1', duration=2)
        SessionTopic.objects.create(session=session, topic=topic)

        payload = {
            'units': [{'num': 1, 'name': 'Нов раздел', 'hours': 5, 'topics': []}],
            'replace_existing': True
        }

        resp = self.client.post(f'/api/subjects/{self.subject.id}/import-curriculum/', payload, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('Не могат да бъдат изтрити съществуващите раздели и теми', resp.data['error'])

    def test_import_curriculum_invalid_payload(self):
        # Empty units
        resp = self.client.post(f'/api/subjects/{self.subject.id}/import-curriculum/', {'units': []}, format='json')
        self.assertEqual(resp.status_code, 400)

        # Missing unit name
        resp2 = self.client.post(f'/api/subjects/{self.subject.id}/import-curriculum/', {
            'units': [{'num': 1, 'name': '', 'hours': 4}]
        }, format='json')
        self.assertEqual(resp2.status_code, 400)

    def test_curriculum_system_prompts_exist(self):
        prompt_base = AIPrompt.objects.filter(page_key='course_units', is_system=True, order=2).first()
        self.assertIsNotNone(prompt_base)
        self.assertIn('MoSCoW', prompt_base.title)

        prompt_stack = AIPrompt.objects.filter(page_key='course_units', is_system=True, order=3).first()
        self.assertIsNotNone(prompt_stack)
        self.assertIn('Python', prompt_stack.title)
        self.assertIn('Django', prompt_stack.title)
        self.assertIn('Vue', prompt_stack.title)
        self.assertIn('Bootstrap', prompt_stack.title)
        self.assertIn('Python', prompt_stack.prompt_text)
        self.assertIn('Django', prompt_stack.prompt_text)
        self.assertIn('Vue.js', prompt_stack.prompt_text)


class GoalImportAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='teacher_goals', password='password123')
        self.client.force_authenticate(user=self.user)
        self.subject = Subject.objects.create(name='Програмиране', grade=10, subject_type='теория', hpy=72)

    def test_import_goals_replace_mode(self):
        Goal.objects.create(course=self.subject, num=1, name='Стара цел 1')
        Goal.objects.create(course=self.subject, num=2, name='Стара цел 2')

        payload = {
            'goals': [
                {'num': 1, 'name': 'Дефинира основни типове данни'},
                {'num': 2, 'name': 'Проектира модулни функции'},
                {'num': 3, 'name': 'Прилага алгоритми за сортиране'}
            ],
            'replace_existing': True
        }

        resp = self.client.post(f'/api/subjects/{self.subject.id}/import-goals/', payload, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Успешно бяха импортирани 3 цели', resp.data['message'])

        goals = Goal.objects.filter(course=self.subject).order_by('num')
        self.assertEqual(goals.count(), 3)
        self.assertEqual(goals[0].name, 'Дефинира основни типове данни')
        self.assertEqual(goals[2].name, 'Прилага алгоритми за сортиране')

    def test_import_goals_append_mode(self):
        Goal.objects.create(course=self.subject, num=1, name='Базова цел 1')

        payload = {
            'goals': [
                {'num': 1, 'name': 'Надграждаща цел 2'}
            ],
            'replace_existing': False
        }

        resp = self.client.post(f'/api/subjects/{self.subject.id}/import-goals/', payload, format='json')
        self.assertEqual(resp.status_code, 200)

        goals = Goal.objects.filter(course=self.subject).order_by('num')
        self.assertEqual(goals.count(), 2)
        self.assertEqual(goals[0].name, 'Базова цел 1')
        self.assertEqual(goals[1].name, 'Надграждаща цел 2')
        self.assertEqual(goals[1].num, 2)

    def test_import_goals_raw_json_and_validation(self):
        # Valid raw_json string
        payload_raw = {
            'raw_json': '[{"num": 1, "name": "Цел от raw json"}]',
            'replace_existing': True
        }
        resp = self.client.post(f'/api/subjects/{self.subject.id}/import-goals/', payload_raw, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Goal.objects.filter(course=self.subject, name='Цел от raw json').exists())

        # Empty list -> 400
        resp_empty = self.client.post(f'/api/subjects/{self.subject.id}/import-goals/', {'goals': []}, format='json')
        self.assertEqual(resp_empty.status_code, 400)

        # Missing goal name -> 400
        resp_noname = self.client.post(f'/api/subjects/{self.subject.id}/import-goals/', {
            'goals': [{'num': 1, 'name': ''}]
        }, format='json')
        self.assertEqual(resp_noname.status_code, 400)

    def test_goals_system_prompt_exists(self):
        prompt = AIPrompt.objects.filter(page_key='course_goals', is_system=True).first()
        self.assertIsNotNone(prompt)
        self.assertIn('таксономията на Блум', prompt.title)


class SessionImportAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='teacher_sessions', password='password123')
        self.client.force_authenticate(user=self.user)
        self.subject = Subject.objects.create(name='Обектно-ориентирано програмиране', grade=10, subject_type='теория', hpy=72, hpw1=2, hpw2=2)
        self.unit1 = Unit.objects.create(subject=self.subject, num=1, name='Основи на ООП', hours=8)
        self.topic1 = Topic.objects.create(unit=self.unit1, num=1, name='Класове и обекти', MoSCoW_cat='M', MoSCoW_rem='База')
        self.topic2 = Topic.objects.create(unit=self.unit1, num=2, name='Конструктори и деструктори', MoSCoW_cat='S', MoSCoW_rem='Важно')
        self.unit2 = Unit.objects.create(subject=self.subject, num=2, name='Наследяване', hours=10)
        self.topic3 = Topic.objects.create(unit=self.unit2, num=1, name='Базови и производни класове', MoSCoW_cat='M', MoSCoW_rem='Ядро')

    def test_import_sessions_replace_mode(self):
        # Create an old session that should be replaced
        old_session = Session.objects.create(course=self.subject, num=1, name='Стар урок за изтриване', duration=2)

        payload = {
            'sessions': [
                {
                    'num': 1,
                    'name': 'Въведение в класове и обекти',
                    'session_type': 'НЗ',
                    'duration': 2,
                    'basic_level': True,
                    'goals': '1. Дефинира клас;\n2. Инстанцира обект.',
                    'focus': 'Синтаксис на клас, полета и методи.',
                    'topics': [
                        {
                            'unit_num': 1,
                            'topic_num': 1,
                            'description': 'Теоретично въведение и код'
                        }
                    ]
                },
                {
                    'num': 2,
                    'name': 'Практикум: Конструктори и методи',
                    'session_type': 'УПР',
                    'duration': 2,
                    'basic_level': True,
                    'goals': '1. Използва конструктори с параметри.',
                    'focus': 'Практическо решаване на задачи.',
                    'topics': [
                        {
                            'name': 'Конструктори и деструктори',
                            'description': 'Задачи за упражнение'
                        }
                    ]
                }
            ],
            'replace_existing': True
        }

        resp = self.client.post(f'/api/subjects/{self.subject.id}/import-sessions/', payload, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Успешно бяха импортирани 2 урока', resp.data['message'])

        sessions = Session.objects.filter(course=self.subject).order_by('num')
        self.assertEqual(sessions.count(), 2)
        self.assertFalse(Session.objects.filter(id=old_session.id).exists())

        s1 = sessions[0]
        self.assertEqual(s1.name, 'Въведение в класове и обекти')
        self.assertEqual(s1.session_type, 'НЗ')
        self.assertEqual(s1.duration, 2)
        self.assertEqual(s1.session_topics.count(), 1)
        self.assertEqual(s1.session_topics.first().topic, self.topic1)

        s2 = sessions[1]
        self.assertEqual(s2.name, 'Практикум: Конструктори и методи')
        self.assertEqual(s2.session_type, 'УПР')
        self.assertEqual(s2.session_topics.count(), 1)
        self.assertEqual(s2.session_topics.first().topic, self.topic2)

    def test_import_sessions_append_mode(self):
        Session.objects.create(course=self.subject, num=1, name='Първи базов урок', duration=2)

        payload = {
            'sessions': [
                {
                    'num': 1,
                    'name': 'Втори добавен урок',
                    'session_type': 'НЗ',
                    'duration': 2,
                    'basic_level': True,
                    'goals': 'Цели',
                    'focus': 'Фокус'
                }
            ],
            'replace_existing': False
        }

        resp = self.client.post(f'/api/subjects/{self.subject.id}/import-sessions/', payload, format='json')
        self.assertEqual(resp.status_code, 200)

        sessions = Session.objects.filter(course=self.subject).order_by('num')
        self.assertEqual(sessions.count(), 2)
        self.assertEqual(sessions[0].name, 'Първи базов урок')
        self.assertEqual(sessions[1].name, 'Втори добавен урок')
        self.assertEqual(sessions[1].num, 2)

    def test_import_sessions_raw_json_and_validation(self):
        payload_raw = {
            'raw_json': '[{"num": 1, "name": "Урок от raw json", "session_type": "K", "duration": 3}]',
            'replace_existing': True
        }
        resp = self.client.post(f'/api/subjects/{self.subject.id}/import-sessions/', payload_raw, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Session.objects.filter(course=self.subject, name='Урок от raw json', duration=3).exists())

        # Empty list -> 400
        resp_empty = self.client.post(f'/api/subjects/{self.subject.id}/import-sessions/', {'sessions': []}, format='json')
        self.assertEqual(resp_empty.status_code, 400)

        # Missing session name -> 400
        resp_noname = self.client.post(f'/api/subjects/{self.subject.id}/import-sessions/', {
            'sessions': [{'num': 1, 'name': ''}]
        }, format='json')
        self.assertEqual(resp_noname.status_code, 400)

    def test_lessons_system_prompt_exists(self):
        prompt_theory = AIPrompt.objects.filter(page_key='course_lessons', is_system=True, order=1).first()
        self.assertIsNotNone(prompt_theory)
        self.assertIn('BOPPPS', prompt_theory.title)

        prompt_practice = AIPrompt.objects.filter(page_key='course_lessons', is_system=True, order=2).first()
        self.assertIsNotNone(prompt_practice)
        self.assertIn('Практика', prompt_practice.title)

        prompt_excel = AIPrompt.objects.filter(page_key='course_lessons', is_system=True, order=3).first()
        self.assertIsNotNone(prompt_excel)
        self.assertIn('Excel', prompt_excel.title)
        self.assertIn('topic_plan_template.xlsx', prompt_excel.title)
        self.assertIn('{списък_уроци}', prompt_excel.prompt_text)

        prompt_word = AIPrompt.objects.filter(page_key='course_lessons', is_system=True, order=4).first()
        self.assertIsNotNone(prompt_word)
        self.assertIn('Word', prompt_word.title)
        self.assertIn('Шаблон Тематично разпределение.docx', prompt_word.title)
        self.assertIn('{списък_уроци}', prompt_word.prompt_text)


class SessionPlanImportAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='teacher_plan', password='password123')
        self.client.force_authenticate(user=self.user)
        self.subject = Subject.objects.create(
            name='Обектно-ориентирано програмиране',
            grade=10,
            subject_type='теория',
            hpy=72,
            hpw1=2,
            hpw2=2
        )
        self.session = Session.objects.create(
            course=self.subject,
            num=1,
            name='Въведение в класове и обекти',
            duration=2,
            session_type='НЗ',
            goals='Базови цели',
            focus='Базов фокус'
        )

    def test_import_plan_replace_mode(self):
        # Създаваме предварителна точка
        SessionPoint.objects.create(session=self.session, num=1, name='Стара точка', duration=10)
        SessionNote.objects.create(session=self.session, num=1, name='Стара бележка', content='Старо')
        SessionTask.objects.create(session=self.session, num=1, name='Стара задача', condition='Старо', answer='Старо')

        payload = {
            'replace_existing': True,
            'plan': {
                'goals': '1. Разбира концепцията за клас; 2. Създава инстанции.',
                'focus': 'Синтаксис на class, конструктор __init__ и атрибути.',
                'points': [
                    {
                        'num': 1,
                        'name': 'Bridge-In: Мотивация и софтуерен казус',
                        'description': 'Въведение',
                        'duration': 5,
                        'content': '<p>Казус от практиката</p>'
                    },
                    {
                        'num': 2,
                        'name': 'Презентация и демо��страция на демо код',
                        'description': 'GRR: Директно обучение',
                        'duration': 15,
                        'content': '<p>Демонстрация на код</p>'
                    },
                    {
                        'num': 3,
                        'name': 'Съвместно упражнение',
                        'description': 'GRR: Ръководена практика',
                        'duration': 10,
                        'content': '<p>Писане на код заедно</p>'
                    }
                ],
                'notes': [
                    {
                        'num': 1,
                        'name': 'Теоретичен конспект: Класове',
                        'point_num': 2,
                        'content': '<pre><code>class Dog: pass</code></pre>'
                    }
                ],
                'tasks': [
                    {
                        'num': 1,
                        'name': 'Съвместна задача за клас Student',
                        'point_num': 3,
                        'condition': '<p>Създайте клас Student</p>',
                        'answer': '<pre><code>class Student: pass</code></pre>'
                    }
                ]
            }
        }

        resp = self.client.post(f'/api/sessions/{self.session.id}/import-plan/', payload, format='json')
        self.assertEqual(resp.status_code, 200)

        # Проверка на обновения урок
        self.session.refresh_from_db()
        self.assertIn('Разбира концепцията за клас', self.session.goals)
        self.assertIn('Синтаксис на class', self.session.focus)

        # Проверка на точките
        points = SessionPoint.objects.filter(session=self.session).order_by('num')
        self.assertEqual(points.count(), 3)
        self.assertEqual(points[0].name, 'Bridge-In: Мотивация и софтуерен казус')
        self.assertEqual(points[1].duration, 15)

        # Проверка на бележките и връзката с точка от плана
        notes = SessionNote.objects.filter(session=self.session)
        self.assertEqual(notes.count(), 1)
        self.assertEqual(notes[0].point, points[1])  # point_num 2 -> points[1]
        self.assertIn('class Dog', notes[0].content)

        tasks = SessionTask.objects.filter(session=self.session)
        self.assertEqual(tasks.count(), 1)
        self.assertEqual(tasks[0].point, points[2])  # point_num 3 -> points[2]
        self.assertIn('Student', tasks[0].condition)
        self.assertIn('class Student', tasks[0].answer)

    def test_import_plan_append_mode(self):
        SessionPoint.objects.create(session=self.session, num=1, name='Първоначална точка', duration=10)

        payload = {
            'replace_existing': False,
            'plan': {
                'points': [
                    {
                        'num': 1,
                        'name': 'Добавена нова точка',
                        'duration': 15
                    }
                ]
            }
        }

        resp = self.client.post(f'/api/sessions/{self.session.id}/import-plan/', payload, format='json')
        self.assertEqual(resp.status_code, 200)

        points = SessionPoint.objects.filter(session=self.session).order_by('num')
        self.assertEqual(points.count(), 2)
        self.assertEqual(points[0].name, 'Първоначална точка')
        self.assertEqual(points[1].name, 'Добавена нова точка')
        self.assertEqual(points[1].num, 2)

    def test_import_plan_validation(self):
        # Empty payload -> 400
        resp_empty = self.client.post(f'/api/sessions/{self.session.id}/import-plan/', {}, format='json')
        self.assertEqual(resp_empty.status_code, 400)

        # Points not a list -> 400
        resp_invalid = self.client.post(f'/api/sessions/{self.session.id}/import-plan/', {
            'plan': {'points': 'not-a-list'}
        }, format='json')
        self.assertEqual(resp_invalid.status_code, 400)

    def test_lesson_plan_system_prompt_exists(self):
        prompt = AIPrompt.objects.filter(page_key='lesson_main', is_system=True, order=1).first()
        self.assertIsNotNone(prompt)
        self.assertIn('BOPPPS', prompt.title)

        notes_prompt = AIPrompt.objects.filter(page_key='lesson_main', is_system=True, order=2).first()
        self.assertIsNotNone(notes_prompt)
        self.assertIn('теоретични бележки', notes_prompt.title)

    def test_lesson_view_and_expanded_context_contains_grade(self):
        # Достъпване на изгледа за урок обновява профила на потребителя със съответния урок и предмет
        self.client.force_login(self.user)
        resp = self.client.get(f'/lesson/{self.session.id}/')
        self.assertEqual(resp.status_code, 200)

        self.user.userprofile.refresh_from_db()
        self.assertEqual(self.user.userprofile.session, self.session)
        self.assertEqual(self.user.userprofile.subject, self.subject)

        # Проверка на API контекста за наличието на клас в профила и предмета
        resp_ctx = self.client.get('/api/context/expanded/')
        self.assertEqual(resp_ctx.status_code, 200)
        self.assertEqual(resp_ctx.data['profile']['subject']['grade'], 10)
        self.assertEqual(resp_ctx.data['profile']['subject']['name'], 'Обектно-ориентирано програмиране')


class MediaServingTest(TestCase):
    def test_media_serving_endpoint(self):
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile

        # Създаване на тестов медиен файл
        test_path = default_storage.save("sys_pics/test_logo.png", ContentFile(b"fake-image-bytes"))
        resp = self.client.get(f"/media/{test_path}")
        self.assertEqual(resp.status_code, 200)
        content = b"".join(resp.streaming_content)
        self.assertEqual(content, b"fake-image-bytes")
        resp.close()
        if default_storage.exists(test_path):
            default_storage.delete(test_path)


class SubjectOrderingTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)
        self.school = School.objects.create(full_name='Тестово училище', short_name='ТУ', city='София')
        self.specialty = Specialty.objects.create(school=self.school, specialty_name='Информатика')

        # Създаваме предмети в разбъркан ред
        self.s1 = Subject.objects.create(name='Програмиране', subject_type='практика', grade=10)
        self.s2 = Subject.objects.create(name='Алгоритми', subject_type='практика', grade=10)
        self.s3 = Subject.objects.create(name='Програмиране', subject_type='теория', grade=10)
        self.s4 = Subject.objects.create(name='Алгоритми', subject_type='теория', grade=10)
        self.s5 = Subject.objects.create(name='Бази данни', subject_type='теория', grade=10)
        self.specialty.subjects.add(self.s1, self.s2, self.s3, self.s4, self.s5)

    def test_subject_model_default_ordering(self):
        subjects = list(Subject.objects.all())
        expected = [
            (self.s4.name, self.s4.subject_type),  # Алгоритми - теория
            (self.s2.name, self.s2.subject_type),  # Алгоритми - практика
            (self.s5.name, self.s5.subject_type),  # Бази данни - теория
            (self.s3.name, self.s3.subject_type),  # Програмиране - теория
            (self.s1.name, self.s1.subject_type),  # Програмиране - практика
        ]
        actual = [(s.name, s.subject_type) for s in subjects]
        self.assertEqual(actual, expected)

    def test_specialty_subjects_api_ordering(self):
        resp = self.client.get(f'/api/specialty/{self.specialty.id}/subjects/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        actual = [(s['name'], s['subject_type']) for s in resp.data]
        expected = [
            ('Алгоритми', 'теория'),
            ('Алгоритми', 'практика'),
            ('Бази данни', 'теория'),
            ('Програмиране', 'теория'),
            ('Програмиране', 'практика'),
        ]
        self.assertEqual(actual, expected)


class ItemDeletionApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)
        self.school = School.objects.create(full_name='Тестово училище', short_name='ТУ', city='София')
        self.specialty = Specialty.objects.create(specialty_num='100', specialty_name='Информатика')
        self.school.specialities.add(self.specialty)
        self.subject = Subject.objects.create(name='Програмиране', subject_type='теория', grade=10)
        self.specialty.subjects.add(self.subject)
        self.goal = Goal.objects.create(num=1, name='Основни концепции', course=self.subject)
        self.unit = Unit.objects.create(num=1, name='Увод', hours=10, subject=self.subject)
        self.topic = Topic.objects.create(num=1, name='Синтаксис', unit=self.unit)
        self.session = Session.objects.create(course=self.subject, num=1, name='Урок 1')
        self.session_topic = SessionTopic.objects.create(session=self.session, topic=self.topic)

    def test_delete_specialty(self):
        resp = self.client.delete(f'/api/schools/{self.school.id}/specialty/{self.specialty.id}/')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Specialty.objects.filter(id=self.specialty.id).exists())

    def test_delete_subject(self):
        resp = self.client.delete(f'/api/specialty/{self.specialty.id}/subjects/{self.subject.id}/')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Subject.objects.filter(id=self.subject.id).exists())

    def test_delete_goal(self):
        resp = self.client.delete(f'/api/goals/{self.goal.id}/')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Goal.objects.filter(id=self.goal.id).exists())

    def test_delete_topic_with_session_topic_protection_handled(self):
        resp = self.client.delete(f'/api/topics/{self.topic.id}/')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Topic.objects.filter(id=self.topic.id).exists())
        self.assertFalse(SessionTopic.objects.filter(id=self.session_topic.id).exists())

    def test_delete_unit_with_topics(self):
        resp = self.client.delete(f'/api/units/{self.unit.id}/')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Unit.objects.filter(id=self.unit.id).exists())
        self.assertFalse(Topic.objects.filter(id=self.topic.id).exists())
        self.assertFalse(SessionTopic.objects.filter(id=self.session_topic.id).exists())


class FileUploadAsciiSafetyTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='upload_tester', password='password123')
        self.client.force_authenticate(user=self.user)
        self.subject = Subject.objects.create(name='Информатика', subject_type='теория', grade=10)
        self.session = Session.objects.create(course=self.subject, num=1, name='Урок 1: Архитектура')

    def test_generate_unique_ascii_filename_with_cyrillic(self):
        from main.utils import generate_unique_ascii_filename

        cyrillic_name = "Тематично разпределение за 10 клас.DOCX"
        safe_name = generate_unique_ascii_filename(cyrillic_name)

        # Трябва да съдържа само ASCII шестнадесетични знаци и разширение .docx
        self.assertTrue(re.match(r'^[a-f0-9]{32}\.docx$', safe_name))
        self.assertTrue(safe_name.isascii())

        # Генерирането на ново име за същия файл трябва да е уникално
        safe_name_2 = generate_unique_ascii_filename(cyrillic_name)
        self.assertNotEqual(safe_name, safe_name_2)

    def test_session_attachment_upload_cyrillic_filename_saves_as_ascii(self):
        uploaded_file = SimpleUploadedFile(
            'Тематичен_План_2026.docx',
            b'word-binary-content',
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

        resp = self.client.post('/api/session-attachments/upsert/', {
            'session': self.session.id,
            'name': 'Тематичен план 2026',
            'file': uploaded_file,
            'attachment_type': 'other'
        }, format='multipart')

        self.assertEqual(resp.status_code, 201)
        attachment = SessionAttachment.objects.get(id=resp.data['id'])

        # Името в базата / UI се запазва четимо
        self.assertEqual(attachment.name, 'Тематичен план 2026')

        # Физическият файл на диска е в session_attachments/ с безопасно ASCII име
        self.assertTrue(attachment.file.name.startswith('session_attachments/'))
        self.assertTrue(attachment.file.name.isascii())
        self.assertTrue(re.search(r'session_attachments/[a-f0-9]{32}\.docx$', attachment.file.name))

        # Почистване
        if attachment.file and default_storage.exists(attachment.file.name):
            default_storage.delete(attachment.file.name)

    def test_app_attachment_upload_cyrillic_filename_saves_as_ascii(self):
        uploaded_file = SimpleUploadedFile(
            'Наредба_№5_на_МОН.pdf',
            b'%PDF-1.4 sample content',
            content_type='application/pdf'
        )

        resp = self.client.post('/api/app-attachments/upsert/', {
            'name': 'Наредба №5 на МОН',
            'file': uploaded_file,
            'num': 1
        }, format='multipart')

        self.assertEqual(resp.status_code, 201)
        app_att = AppAttachment.objects.get(id=resp.data['id'])

        self.assertEqual(app_att.name, 'Наредба №5 на МОН')
        self.assertTrue(app_att.file.name.startswith('app_attachments/'))
        self.assertTrue(app_att.file.name.isascii())
        self.assertTrue(re.search(r'app_attachments/[a-f0-9]{32}\.pdf$', app_att.file.name))

        # Почистване
        if app_att.file and default_storage.exists(app_att.file.name):
            default_storage.delete(app_att.file.name)

    def test_image_upload_with_cyrillic_filename(self):
        image_file = SimpleUploadedFile(
            'Схема на алгоритъм.png',
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR',
            content_type='image/png'
        )

        resp = self.client.post('/api/uploads/tinymce-image/', {
            'file': image_file
        }, format='multipart')

        self.assertEqual(resp.status_code, 201)
        location = resp.data.get('location', '')
        self.assertTrue(location.isascii())
        self.assertIn('/media/session_pics/img_', location)
        self.assertTrue(location.endswith('.png'))

        # Извличане на относителния път за изтриване
        rel_path = location.split('/media/')[-1]
        if default_storage.exists(rel_path):
            default_storage.delete(rel_path)
