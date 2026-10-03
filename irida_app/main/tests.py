import re
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from main.constants import STUDENT, TEACHER, SUPERADMIN, SCHOOLADMIN
from main.models import (
    AIPrompt,
    AppAttachment,
    BroadcastMessage,
    BroadcastMessageRead,
    Goal,
    Log,
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

    def test_create_large_attachment(self):
        # Test uploading a large file (~28MB) such as a PowerPoint presentation
        large_content = b'0' * (28 * 1024 * 1024)
        large_file = SimpleUploadedFile("Презентация_1.pptx", large_content, content_type="application/vnd.openxmlformats-officedocument.presentationml.presentation")
        create_data = {
            'id': 0,
            'session': self.session.id,
            'point': '',
            'num': 1,
            'name': 'Презентация 1',
            'attachment_type': 'other',
            'description': 'Голяма презентация',
            'file': large_file
        }
        resp = self.client.post('/api/session-attachments/upsert/', create_data, format='multipart')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['original_filename'], 'Презентация_1.pptx')
        self.assertTrue(resp.data['file_url'].endswith('.pptx'))


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

    def test_student_attachment_visibility_filtering(self):
        # 1. Създаваме разнообразни приложения:
        # self.attachment е 'Теория 1' (theory, is_student_visible=True по подразбиране)
        att_other_visible = SessionAttachment.objects.create(
            session=self.session, num=2, name='Приложение видимо',
            attachment_type='other', is_student_visible=True
        )
        att_other_hidden = SessionAttachment.objects.create(
            session=self.session, num=3, name='Приложение скрито',
            attachment_type='other', is_student_visible=False
        )
        att_theory_flagged_false = SessionAttachment.objects.create(
            session=self.session, num=4, name='Теория 2',
            attachment_type='theory', is_student_visible=False
        )

        # 2. Проверка за ученик през sessions-with-topics
        student_client = APIClient()
        student_client.force_authenticate(user=self.student_user)
        resp_student = student_client.get(f'/api/subjects/{self.subject.id}/sessions-with-topics/')
        self.assertEqual(resp_student.status_code, 200)
        student_att_names = [a['name'] for a in resp_student.data[0]['session_attachments']]
        self.assertIn('Теория 1', student_att_names)
        self.assertIn('Приложение видимо', student_att_names)
        self.assertIn('Теория 2', student_att_names)  # Теорията е по подразбиране видима за учениците
        self.assertNotIn('Приложение скрито', student_att_names)
        self.assertEqual(len(student_att_names), 3)

        # 3. Проверка за ученик през direct session attachments endpoint
        resp_student_direct = student_client.get(f'/api/sessions/{self.session.id}/attachments/')
        self.assertEqual(resp_student_direct.status_code, 200)
        direct_names = [a['name'] for a in resp_student_direct.data]
        self.assertIn('Теория 1', direct_names)
        self.assertIn('Приложение видимо', direct_names)
        self.assertIn('Теория 2', direct_names)
        self.assertNotIn('Приложение скрито', direct_names)
        self.assertEqual(len(direct_names), 3)

        # 4. Проверка за учител през sessions-with-topics
        teacher_client = APIClient()
        teacher_client.force_authenticate(user=self.teacher_user)
        resp_teacher = teacher_client.get(f'/api/subjects/{self.subject.id}/sessions-with-topics/')
        self.assertEqual(resp_teacher.status_code, 200)
        teacher_att_names = [a['name'] for a in resp_teacher.data[0]['session_attachments']]
        self.assertEqual(len(teacher_att_names), 4)
        self.assertIn('Приложение скрито', teacher_att_names)

        # 5. Проверка за учител през direct session attachments endpoint
        resp_teacher_direct = teacher_client.get(f'/api/sessions/{self.session.id}/attachments/')
        self.assertEqual(resp_teacher_direct.status_code, 200)
        self.assertEqual(len(resp_teacher_direct.data), 4)

    def test_session_attachment_upsert_is_student_visible_flag(self):
        client = APIClient()
        client.force_authenticate(user=self.teacher_user)

        # Създаване на скрито приложение с 'false' низ
        resp = client.post('/api/session-attachments/upsert/', {
            'session': self.session.id,
            'name': 'Само за учители',
            'attachment_type': 'other',
            'is_student_visible': 'false'
        })
        self.assertEqual(resp.status_code, 201)
        att_id = resp.data['id']
        att = SessionAttachment.objects.get(id=att_id)
        self.assertFalse(att.is_student_visible)
        self.assertFalse(resp.data['is_student_visible'])

        # Редакция на същото приложение до видимо с 'true'
        resp_update = client.post('/api/session-attachments/upsert/', {
            'id': att_id,
            'is_student_visible': 'true'
        })
        self.assertEqual(resp_update.status_code, 200)
        att.refresh_from_db()
        self.assertTrue(att.is_student_visible)
        self.assertTrue(resp_update.data['is_student_visible'])

    def test_student_feedback_upload_attachment(self):
        student_client = APIClient()
        student_client.force_authenticate(user=self.student_user)

        test_file = SimpleUploadedFile("zadacha_reshenie.docx", b"Word content", content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        full_name = f"{self.student_user.first_name} {self.student_user.last_name}"

        # 1. Изпращане на обратна връзка от ученика като задача
        resp = student_client.post('/api/session-attachments/upsert/', {
            'id': 0,
            'session': self.session.id,
            'name': full_name,
            'attachment_type': 'task',
            'is_student_visible': 'false',
            'description': f'Обратна връзка: {full_name}',
            'file': test_file
        }, format='multipart')

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        att_id = resp.data['id']
        att = SessionAttachment.objects.get(id=att_id)
        self.assertEqual(att.session, self.session)
        self.assertIsNone(att.point)
        self.assertEqual(att.name, full_name)
        self.assertEqual(att.attachment_type, 'task')
        self.assertFalse(att.is_student_visible)
        self.assertEqual(att.description, f'Обратна връзка: {full_name}')

        # 2. Проверка, че прикаченият файл НЕ е видим за ученика в sessions-with-topics
        resp_student_sessions = student_client.get(f'/api/subjects/{self.subject.id}/sessions-with-topics/')
        self.assertEqual(resp_student_sessions.status_code, 200)
        student_attachments = resp_student_sessions.data[0]['session_attachments']
        student_att_ids = [a['id'] for a in student_attachments]
        self.assertNotIn(att_id, student_att_ids)

        # 3. Проверка, че прикаченият файл Е видим за учителя
        teacher_client = APIClient()
        teacher_client.force_authenticate(user=self.teacher_user)
        resp_teacher = teacher_client.get(f'/api/sessions/{self.session.id}/attachments/')
        self.assertEqual(resp_teacher.status_code, 200)
        teacher_att_ids = [a['id'] for a in resp_teacher.data]
        self.assertIn(att_id, teacher_att_ids)

    def test_user_data_expanded_includes_first_and_last_name(self):
        client = APIClient()
        client.force_authenticate(user=self.student_user)
        resp = client.get('/api/context/expanded/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['first_name'], 'Иван')
        self.assertEqual(resp.data['last_name'], 'Иванов')
        self.assertEqual(resp.data['user_name'], 'Иван Иванов')


class AIPromptAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.teacher_user = User.objects.create_user(username='teacher_ai', password='password123', first_name='Иван', last_name='Иванов')
        self.other_teacher = User.objects.create_user(username='other_teacher_ai', password='password123', first_name='Петър', last_name='Петров')
        self.admin_user = User.objects.create_superuser(username='admin_ai', password='password123', email='admin@test.com')
        self.client.force_authenticate(user=self.teacher_user)

    def test_list_prompts_with_page_key(self):
        # Create sample prompt
        prompt = AIPrompt.objects.create(
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
        item = next(p for p in resp.data if p['id'] == prompt.id)
        self.assertEqual(item['title'], 'Тест промпт за урок')
        self.assertTrue(item['is_author'])
        self.assertTrue(item['can_edit'])
        self.assertTrue(item['can_delete'])

        # Check for another teacher
        client2 = APIClient()
        client2.force_authenticate(user=self.other_teacher)
        resp2 = client2.get('/api/prompts/?page_key=lesson_main')
        item2 = next(p for p in resp2.data if p['id'] == prompt.id)
        self.assertFalse(item2['is_author'])
        self.assertFalse(item2['can_edit'])
        self.assertFalse(item2['can_delete'])

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
        self.assertTrue(resp.data['is_author'])
        self.assertTrue(resp.data['can_edit'])

        # Update by author
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

        # Update by other teacher should be forbidden 403
        client_other = APIClient()
        client_other.force_authenticate(user=self.other_teacher)
        resp_unauth = client_other.post('/api/prompts/upsert/', {
            'id': created_id,
            'title': 'Неоторизирана промяна',
            'page_key': 'lesson_main',
            'prompt_text': 'Хакнат текст',
        }, format='json')
        self.assertEqual(resp_unauth.status_code, 403)

    def test_lesson_main_seeded_micro_prompts(self):
        resp = self.client.get('/api/prompts/?page_key=lesson_main')
        self.assertEqual(resp.status_code, 200)
        titles = [p['title'] for p in resp.data]
        self.assertIn('Критериална матрица, чек-лист за самооценка и изходен билет (Exit Ticket)', titles)
        self.assertIn('Диференцирани работни карти и карти за подкрепа при затруднения (Scaffolding)', titles)
        self.assertIn('Социално-емоционални цели, екипни роли и правила за лабораторно занятие', titles)
        self.assertIn('Предварителна оценка на урок (Стандарт за качество / Оценъчна карта)', titles)
        self.assertIn('Попълване на бланка за планиране на урок (ПГЕЕ / .docx шаблон)', titles)

    def test_delete_user_prompt(self):
        prompt = AIPrompt.objects.create(
            title='За изтриване',
            page_key='lesson_main',
            prompt_text='Текст',
            is_system=False,
            created_by=self.teacher_user
        )
        # Other teacher tries to delete -> 403
        client_other = APIClient()
        client_other.force_authenticate(user=self.other_teacher)
        resp_other = client_other.delete(f'/api/prompts/{prompt.id}/')
        self.assertEqual(resp_other.status_code, 403)
        self.assertTrue(AIPrompt.objects.filter(id=prompt.id).exists())

        # Author deletes -> 204
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
        self.assertContains(resp, f'предмет: {self.subject.name} ({self.subject.subject_type})')

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
        self.assertEqual(app_att.original_filename, 'Наредба_№5_на_МОН.pdf')
        self.assertEqual(resp.data['original_filename'], 'Наредба_№5_на_МОН.pdf')
        self.assertEqual(resp.data['file_name'], 'Наредба_№5_на_МОН.pdf')
        self.assertTrue(app_att.file.name.startswith('app_attachments/'))
        self.assertTrue(app_att.file.name.isascii())
        self.assertTrue(re.search(r'app_attachments/[a-f0-9]{32}\.pdf$', app_att.file.name))

        # Почистване
        if app_att.file and default_storage.exists(app_att.file.name):
            default_storage.delete(app_att.file.name)

    def test_app_attachment_markdown_conversion_original_filename(self):
        md_file = SimpleUploadedFile(
            'Урок_1_Въведение.md',
            b'# Introduction\nSome markdown text.',
            content_type='text/markdown'
        )

        resp = self.client.post('/api/app-attachments/upsert/', {
            'name': 'Урок 1',
            'file': md_file,
            'num': 2,
            'target_format': 'docx'
        }, format='multipart')

        self.assertEqual(resp.status_code, 201)
        app_att = AppAttachment.objects.get(id=resp.data['id'])

        self.assertEqual(app_att.original_filename, 'Урок_1_Въведение.docx')
        self.assertEqual(resp.data['original_filename'], 'Урок_1_Въведение.docx')
        self.assertEqual(resp.data['file_name'], 'Урок_1_Въведение.docx')
        self.assertTrue(app_att.file.name.startswith('app_attachments/'))
        self.assertTrue(app_att.file.name.endswith('.docx'))

        # Почистване
        if app_att.file and default_storage.exists(app_att.file.name):
            default_storage.delete(app_att.file.name)

    def test_app_attachment_update_preserves_or_updates_original_filename(self):
        self.client.force_authenticate(user=self.user)
        f1 = SimpleUploadedFile('Първи_файл.pdf', b'%PDF-1.4 content', content_type='application/pdf')
        resp1 = self.client.post('/api/app-attachments/upsert/', {
            'name': 'Първи файл',
            'file': f1,
            'num': 1
        }, format='multipart')
        self.assertEqual(resp1.status_code, 201)
        att_id = resp1.data['id']
        att = AppAttachment.objects.get(id=att_id)
        self.assertEqual(att.original_filename, 'Първи_файл.pdf')

        # Редакция само на описанието без качване на нов файл -> original_filename се запазва
        resp2 = self.client.post('/api/app-attachments/upsert/', {
            'id': att_id,
            'name': 'Първи файл - редактиран',
            'description': 'Ново описание'
        }, format='multipart')
        self.assertEqual(resp2.status_code, 200)
        att.refresh_from_db()
        self.assertEqual(att.name, 'Първи файл - редактиран')
        self.assertEqual(att.original_filename, 'Първи_файл.pdf')
        self.assertEqual(resp2.data['original_filename'], 'Първи_файл.pdf')

        # Редакция с качване на нов файл -> original_filename се обновява
        f2 = SimpleUploadedFile('Втори_файл.docx', b'DOCX content',
                                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        resp3 = self.client.post('/api/app-attachments/upsert/', {
            'id': att_id,
            'name': 'Втори файл',
            'file': f2
        }, format='multipart')
        self.assertEqual(resp3.status_code, 200)
        att.refresh_from_db()
        self.assertEqual(att.original_filename, 'Втори_файл.docx')
        self.assertEqual(resp3.data['original_filename'], 'Втори_файл.docx')

        # Почистване
        if att.file and default_storage.exists(att.file.name):
            default_storage.delete(att.file.name)

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


class AppAttachmentAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='teacher1', first_name='Иван', last_name='Иванов', password='pass')
        self.user2 = User.objects.create_user(username='teacher2', first_name='Петър', last_name='Петров', password='pass')
        self.admin = User.objects.create_superuser(username='admin', password='adminpass')

    def test_create_attachment_sets_author_and_system_flag(self):
        self.client.force_authenticate(user=self.user1)
        resp = self.client.post('/api/app-attachments/upsert/', {
            'num': 1,
            'name': 'Учебен план',
            'description': 'Описание на плана',
            'is_system': 'false'
        }, format='multipart')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['created_by'], self.user1.id)
        self.assertEqual(resp.data['created_by_name'], 'Иван Иванов')
        self.assertFalse(resp.data['is_system'])
        self.assertTrue(resp.data['is_owner'])

    def test_list_and_filter_attachments(self):
        # 1. User1 creates normal attachment
        att1 = AppAttachment.objects.create(
            num=1, name='Файл 1', created_by=self.user1, is_system=False
        )
        # 2. User2 creates normal attachment
        att2 = AppAttachment.objects.create(
            num=2, name='Файл 2', created_by=self.user2, is_system=False
        )
        # 3. System attachment
        att3 = AppAttachment.objects.create(
            num=3, name='Системен файл', created_by=self.admin, is_system=True
        )

        self.client.force_authenticate(user=self.user1)

        # All
        resp_all = self.client.get('/api/app-attachments/')
        self.assertEqual(resp_all.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp_all.data), 3)

        # System
        resp_sys = self.client.get('/api/app-attachments/?filter=system')
        self.assertEqual(resp_sys.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp_sys.data), 1)
        self.assertEqual(resp_sys.data[0]['id'], att3.id)

        # Mine
        resp_mine = self.client.get('/api/app-attachments/?filter=mine')
        self.assertEqual(resp_mine.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp_mine.data), 1)
        self.assertEqual(resp_mine.data[0]['id'], att1.id)
        self.assertTrue(resp_mine.data[0]['is_owner'])

    def test_edit_and_delete_permissions(self):
        att1 = AppAttachment.objects.create(
            num=1, name='Файл на Иван', created_by=self.user1, is_system=False
        )

        # User2 tries to edit User1's attachment -> 403 Forbidden
        self.client.force_authenticate(user=self.user2)
        resp_edit_forbidden = self.client.post('/api/app-attachments/upsert/', {
            'id': att1.id,
            'name': 'Хакнато име'
        }, format='multipart')
        self.assertEqual(resp_edit_forbidden.status_code, status.HTTP_403_FORBIDDEN)

        # User2 tries to delete User1's attachment -> 403 Forbidden
        resp_del_forbidden = self.client.delete(f'/api/app-attachments/{att1.id}/')
        self.assertEqual(resp_del_forbidden.status_code, status.HTTP_403_FORBIDDEN)

        # User1 edits own attachment -> 200 OK
        self.client.force_authenticate(user=self.user1)
        resp_edit_ok = self.client.post('/api/app-attachments/upsert/', {
            'id': att1.id,
            'name': 'Обновено име'
        }, format='multipart')
        self.assertEqual(resp_edit_ok.status_code, status.HTTP_200_OK)
        att1.refresh_from_db()
        self.assertEqual(att1.name, 'Обновено име')

        # User1 deletes own attachment -> 204 No Content
        resp_del_ok = self.client.delete(f'/api/app-attachments/{att1.id}/')
        self.assertEqual(resp_del_ok.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(AppAttachment.objects.filter(id=att1.id).exists())

    def test_create_large_app_attachment(self):
        self.client.force_authenticate(user=self.user1)
        large_content = b'0' * (28 * 1024 * 1024)
        large_file = SimpleUploadedFile("Голям_документ.pptx", large_content, content_type="application/vnd.openxmlformats-officedocument.presentationml.presentation")
        resp = self.client.post('/api/app-attachments/upsert/', {
            'id': 0,
            'num': 1,
            'name': '',
            'description': 'Голяма презентация',
            'file': large_file
        }, format='multipart')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['original_filename'], 'Голям_документ.pptx')
        self.assertEqual(resp.data['name'], 'Голям_документ.pptx')
        self.assertTrue(resp.data['file_url'].endswith('.pptx'))


class UserManagementAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(username='admin_main', password='adminpass')
        self.client.force_authenticate(user=self.admin)

    def test_create_administrator_user(self):
        data = {
            'username': 'admin_new',
            'password': 'password123',
            'first_name': 'Администратор',
            'last_name': 'Системен',
            'email': 'admin_new@example.com',
            'userprofile': {
                'gender': True,
                'school': 0,
                'access_level': 3,
                'session_screen': 1,
                'session': 0,
                'grade': 8,
                'section': 'a',
                'speciality': 0,
                'subject': 0,
            }
        }
        resp = self.client.post('/api/users/', data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username='admin_new')
        self.assertEqual(user.first_name, 'Администратор')
        self.assertEqual(user.userprofile.access_level, 3)
        self.assertEqual(user.userprofile.section, 'а')
        self.assertIsNone(user.userprofile.school)

    def test_update_user(self):
        u = User.objects.create_user(username='teacher_edit', first_name='Иван', last_name='Петров')
        u.userprofile.access_level = 4
        u.userprofile.save()

        data = {
            'username': 'teacher_edit',
            'first_name': 'Иван (Редактиран)',
            'last_name': 'Петров',
            'userprofile': {
                'gender': True,
                'access_level': 4,
                'section': 'b',
            }
        }
        resp = self.client.put(f'/api/users/{u.id}/', data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        u.refresh_from_db()
        self.assertEqual(u.first_name, 'Иван (Редактиран)')
        self.assertEqual(u.userprofile.section, 'б')

    def test_school_specialties_for_zero_school(self):
        resp = self.client.get('/api/schools/0/specialties/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, [])

    def test_user_list_view_with_school_zero_and_admin_level(self):
        resp = self.client.get('/api/users-list/0/1/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.data) >= 1)

        # Test school 0 level 3 includes level 3 admin
        resp_admin = self.client.get('/api/users-list/0/3/')
        self.assertEqual(resp_admin.status_code, status.HTTP_200_OK)
        admin_ids = [u['id'] for u in resp_admin.data]
        self.assertIn(self.admin.id, admin_ids)


class SessionAttachmentOriginalFilenameTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='admin_att', password='adminpass')
        self.client.force_authenticate(user=self.user)

        self.school = School.objects.create(short_name='ТУ', full_name='Тестово училище', city='София')
        self.subject = Subject.objects.create(name='Информатика')
        self.session = Session.objects.create(course=self.subject, num=1, name='Урок 1')

    def test_session_attachment_upload_cyrillic_filename(self):
        cyrillic_content = b'Sample content in file'
        uploaded_file = SimpleUploadedFile(
            'Учебен_материал_тест.pdf',
            cyrillic_content,
            content_type='application/pdf'
        )

        resp = self.client.post('/api/session-attachments/upsert/', {
            'id': 0,
            'session': self.session.id,
            'name': 'Материал по теория',
            'attachment_type': 'theory',
            'file': uploaded_file
        }, format='multipart')

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['original_filename'], 'Учебен_материал_тест.pdf')
        self.assertEqual(resp.data['file_name'], 'Учебен_материал_тест.pdf')

        att = SessionAttachment.objects.get(id=resp.data['id'])
        self.assertEqual(att.original_filename, 'Учебен_материал_тест.pdf')

    def test_session_attachment_markdown_conversion_original_filename(self):
        md_content = b'# Heading\nText'
        uploaded_file = SimpleUploadedFile(
            'План_урок_1.md',
            md_content,
            content_type='text/markdown'
        )

        resp = self.client.post('/api/session-attachments/upsert/', {
            'id': 0,
            'session': self.session.id,
            'name': 'План',
            'attachment_type': 'theory',
            'target_format': 'docx',
            'file': uploaded_file
        }, format='multipart')

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['original_filename'], 'План_урок_1.docx')
        self.assertTrue(resp.data['file_name'].endswith('.docx'))

    def test_session_attachment_markdown_to_pdf_with_large_table(self):
        # Създаване на Markdown файл с много голям табличен ред (>1000 символа и <br> елементи)
        large_cell_content = '<br>- '.join([f'Дейност {i}: Обяснение на подробности и примери по темата HTTP' for i in range(1, 15)])
        md_table = f"""# План на урок
| Елемент | Описание |
| --- | --- |
| **Основни цели и дейности**<br>- *Инструкции* | - {large_cell_content} |
"""
        uploaded_file = SimpleUploadedFile(
            'Бланка_урок.md',
            md_table.encode('utf-8'),
            content_type='text/markdown'
        )

        resp = self.client.post('/api/session-attachments/upsert/', {
            'id': 0,
            'session': self.session.id,
            'name': 'Бланка урок',
            'attachment_type': 'theory',
            'target_format': 'pdf',
            'file': uploaded_file
        }, format='multipart')

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['original_filename'], 'Бланка_урок.pdf')
        self.assertTrue(resp.data['file_name'].endswith('.pdf'))

    def test_session_attachment_edit_without_new_file_preserves_original_filename(self):
        att = SessionAttachment.objects.create(
            session=self.session,
            num=1,
            name='Старо заглавие',
            original_filename='Оригинално_име.pdf',
            attachment_type='other'
        )

        resp = self.client.post('/api/session-attachments/upsert/', {
            'id': att.id,
            'session': self.session.id,
            'name': 'Ново заглавие',
            'attachment_type': 'other'
        }, format='multipart')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        att.refresh_from_db()
        self.assertEqual(att.name, 'Ново заглавие')
        self.assertEqual(att.original_filename, 'Оригинално_име.pdf')
        self.assertEqual(resp.data['original_filename'], 'Оригинално_име.pdf')


class Step3FeaturesTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.teacher_user = User.objects.create_user(username='teacher_step3', password='password123')
        self.teacher_user.userprofile.access_level = 4
        self.teacher_user.userprofile.save()
        self.client.force_authenticate(user=self.teacher_user)

        self.subject = Subject.objects.create(name='Интернет програмиране')
        self.session = Session.objects.create(
            course=self.subject,
            num=1,
            name='HTTP протокол',
            goals='Разбиране на клиент-сървър архитектура',
            social_emotional_goals='Сътрудничество при работа по двойки',
            duration=2,
            session_type='НЗ'
        )

    def test_session_social_emotional_goals_crud(self):
        # Read session
        resp = self.client.get(f'/api/sessions/{self.session.id}/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['social_emotional_goals'], 'Сътрудничество при работа по двойки')

        # Update session
        update_payload = {
            'course': self.subject.id,
            'num': 1,
            'name': 'HTTP протокол (обновен)',
            'goals': 'Академични цели',
            'social_emotional_goals': 'Упоритост при откриване на грешки в заявките',
            'duration': 2,
            'session_type': 'НЗ',
            'basic_level': True,
            'collapsed': False
        }
        resp_update = self.client.put(f'/api/sessions/{self.session.id}/', update_payload, format='json')
        self.assertEqual(resp_update.status_code, status.HTTP_200_OK)
        self.session.refresh_from_db()
        self.assertEqual(self.session.social_emotional_goals, 'Упоритост при откриване на грешки в заявките')

    def test_session_attachment_new_types_and_visibility(self):
        # Create worksheet, rubric, exit_ticket
        ws = SessionAttachment.objects.create(
            session=self.session,
            num=1,
            name='Работен лист за HTTP методи',
            attachment_type=SessionAttachment.WORKSHEET,
            is_student_visible=True
        )
        rubric = SessionAttachment.objects.create(
            session=self.session,
            num=2,
            name='Критериална карта за взаимна проверка',
            attachment_type=SessionAttachment.RUBRIC,
            is_student_visible=False
        )
        exit_ticket = SessionAttachment.objects.create(
            session=self.session,
            num=3,
            name='Изходен билет',
            attachment_type=SessionAttachment.EXIT_TICKET,
            is_student_visible=True
        )

        # Teacher sees all 3
        resp_teacher = self.client.get(f'/api/sessions/{self.session.id}/attachments/')
        self.assertEqual(resp_teacher.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp_teacher.data), 3)

        # Student user
        student_user = User.objects.create_user(username='student_step3', password='password123')
        student_user.userprofile.access_level = STUDENT
        student_user.userprofile.save()

        student_client = APIClient()
        student_client.force_authenticate(user=student_user)

        # Student should only see worksheet and exit_ticket (not rubric because is_student_visible=False)
        resp_student = student_client.get(f'/api/sessions/{self.session.id}/attachments/')
        self.assertEqual(resp_student.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp_student.data), 2)
        types_visible = [att['attachment_type'] for att in resp_student.data]
        self.assertIn(SessionAttachment.WORKSHEET, types_visible)
        self.assertIn(SessionAttachment.EXIT_TICKET, types_visible)
        self.assertNotIn(SessionAttachment.RUBRIC, types_visible)


class AuditLoggingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teacher_audit', password='password123')
        self.user.userprofile.access_level = TEACHER
        self.user.userprofile.save()

    def test_audit_login_success_and_logout(self):
        client = Client()
        resp_login = client.post(reverse('login'), {'username': 'teacher_audit', 'password': 'password123'})
        self.assertEqual(resp_login.status_code, 302)

        login_logs = Log.objects.filter(user_name='teacher_audit', action__contains='[LOGIN]')
        self.assertTrue(login_logs.exists())

        resp_logout = client.get(reverse('logout'))
        self.assertEqual(resp_logout.status_code, 302)

        logout_logs = Log.objects.filter(user_name='teacher_audit', action__contains='[LOGOUT]')
        self.assertTrue(logout_logs.exists())

    def test_audit_login_failed(self):
        client = Client()
        resp_login_bad = client.post(reverse('login'), {'username': 'teacher_audit', 'password': 'wrongpassword'})
        self.assertEqual(resp_login_bad.status_code, 200)

        fail_logs = Log.objects.filter(action__contains='[LOGIN_FAILED]')
        self.assertTrue(fail_logs.exists())

    def test_audit_helper_direct(self):
        from main.audit import log_audit_event
        log_audit_event(
            request=None,
            action="TEST_ACTION",
            target_model="TestModel",
            target_id=999,
            status="SUCCESS",
            details="Direct test detail",
            user=self.user,
        )
        direct_logs = Log.objects.filter(action__contains='[TEST_ACTION]')
        self.assertTrue(direct_logs.exists())


class OwnershipAndAuthorizationTest(TestCase):
    def setUp(self):
        self.teacher_a = User.objects.create_user(username='teacher_a', password='password123')
        self.teacher_a.userprofile.access_level = TEACHER
        self.teacher_a.userprofile.save()

        self.teacher_b = User.objects.create_user(username='teacher_b', password='password123')
        self.teacher_b.userprofile.access_level = TEACHER
        self.teacher_b.userprofile.save()

        self.admin_user = User.objects.create_user(username='admin_user', password='password123')
        self.admin_user.userprofile.access_level = SUPERADMIN
        self.admin_user.userprofile.save()

        self.student_user = User.objects.create_user(username='student_u', password='password123')
        self.student_user.userprofile.access_level = STUDENT
        self.student_user.userprofile.save()

        self.school = School.objects.create(full_name='Училище Авторство', short_name='УА', city='София')
        self.specialty = Specialty.objects.create(school=self.school, specialty_name='Информатика')
        self.subject = Subject.objects.create(
            specialty=self.specialty,
            name='Уеб дизайн',
            grade=11,
            creator=self.teacher_a
        )
        self.session_a = Session.objects.create(
            course=self.subject,
            num=1,
            name='Урок на Учител А',
            author=self.teacher_a
        )
        self.session_anon = Session.objects.create(
            course=self.subject,
            num=2,
            name='Анонимен урок',
            author=None
        )

    def test_teacher_b_cannot_edit_or_delete_teacher_a_lesson(self):
        client = APIClient()
        client.force_authenticate(user=self.teacher_b)

        # PUT attempt
        resp_put = client.put(f'/api/sessions/{self.session_a.id}/', {
            'course': self.subject.id,
            'num': 1,
            'name': 'Опит за промяна от Б'
        })
        self.assertEqual(resp_put.status_code, status.HTTP_403_FORBIDDEN)

        # DELETE attempt
        resp_del = client.delete(f'/api/sessions/{self.session_a.id}/')
        self.assertEqual(resp_del.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_a_can_edit_own_lesson(self):
        client = APIClient()
        client.force_authenticate(user=self.teacher_a)

        resp_put = client.put(f'/api/sessions/{self.session_a.id}/', {
            'course': self.subject.id,
            'num': 1,
            'name': 'Обновено име от Учител А'
        })
        self.assertEqual(resp_put.status_code, status.HTTP_200_OK)
        self.session_a.refresh_from_db()
        self.assertEqual(self.session_a.name, 'Обновено име от Учител А')
        self.assertEqual(self.session_a.author, self.teacher_a)

    def test_admin_can_edit_teacher_a_lesson_keeping_author(self):
        client = APIClient()
        client.force_authenticate(user=self.admin_user)

        resp_put = client.put(f'/api/sessions/{self.session_a.id}/', {
            'course': self.subject.id,
            'num': 1,
            'name': 'Коригирана грешка от Админ',
            'keep_original_author': True
        })
        self.assertEqual(resp_put.status_code, status.HTTP_200_OK)
        self.session_a.refresh_from_db()
        self.assertEqual(self.session_a.name, 'Коригирана грешка от Админ')
        self.assertEqual(self.session_a.author, self.teacher_a)

    def test_admin_can_claim_ownership(self):
        client = APIClient()
        client.force_authenticate(user=self.admin_user)

        resp_put = client.put(f'/api/sessions/{self.session_a.id}/', {
            'course': self.subject.id,
            'num': 1,
            'name': 'Присвоен урок от Админ',
            'claim_ownership': True
        })
        self.assertEqual(resp_put.status_code, status.HTTP_200_OK)
        self.session_a.refresh_from_db()
        self.assertEqual(self.session_a.name, 'Присвоен урок от Админ')
        self.assertEqual(self.session_a.author, self.admin_user)

    def test_anonymous_content_claimed_on_first_edit(self):
        client = APIClient()
        client.force_authenticate(user=self.teacher_a)

        self.assertIsNone(self.session_anon.author)
        resp_put = client.put(f'/api/sessions/{self.session_anon.id}/', {
            'course': self.subject.id,
            'num': 2,
            'name': 'Вече авторски урок на А'
        })
        self.assertEqual(resp_put.status_code, status.HTTP_200_OK)
        self.session_anon.refresh_from_db()
        self.assertEqual(self.session_anon.name, 'Вече авторски урок на А')
        self.assertEqual(self.session_anon.author, self.teacher_a)

    def test_point_and_note_and_task_ownership(self):
        # Create point as Teacher A
        client_a = APIClient()
        client_a.force_authenticate(user=self.teacher_a)

        resp_pt = client_a.post('/api/session-points/upsert/', {
            'session': self.session_a.id,
            'num': 1,
            'name': 'Точка 1',
            'duration': 15,
            'content': '<p>Контент</p>'
        })
        self.assertEqual(resp_pt.status_code, status.HTTP_201_CREATED)
        point_id = resp_pt.data['id']

        # Teacher B cannot edit point
        client_b = APIClient()
        client_b.force_authenticate(user=self.teacher_b)

        resp_pt_b = client_b.post('/api/session-points/upsert/', {
            'id': point_id,
            'session': self.session_a.id,
            'num': 1,
            'name': 'Точка 1 от Б',
            'duration': 15,
            'content': '<p>Контент Б</p>'
        })
        self.assertEqual(resp_pt_b.status_code, status.HTTP_403_FORBIDDEN)

        # Teacher B cannot delete point
        resp_pt_del = client_b.delete(f'/api/session-points/{point_id}/')
        self.assertEqual(resp_pt_del.status_code, status.HTTP_403_FORBIDDEN)

        # Teacher A can edit point
        resp_pt_edit = client_a.post('/api/session-points/upsert/', {
            'id': point_id,
            'session': self.session_a.id,
            'num': 1,
            'name': 'Точка 1 променена от А',
            'duration': 20,
            'content': '<p>Контент А нов</p>'
        })
        self.assertEqual(resp_pt_edit.status_code, status.HTTP_200_OK)


class BroadcastMessagesAPITest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin_bcast', password='password123')
        self.admin.userprofile.access_level = SUPERADMIN
        self.admin.userprofile.save()

        self.teacher = User.objects.create_user(username='teacher_bcast', password='password123')
        self.teacher.userprofile.access_level = TEACHER
        self.teacher.userprofile.save()

        self.student = User.objects.create_user(username='student_bcast', password='password123')
        self.student.userprofile.access_level = STUDENT
        self.student.userprofile.save()

        # Message for Teachers only
        self.msg_teacher = BroadcastMessage.objects.create(
            title='Важно за учители',
            message='Срокът за предаване на плановете изтича в петък.',
            target_role=BroadcastMessage.AUDIENCE_TEACHER,
            created_by=self.admin
        )

        # Message for All
        self.msg_all = BroadcastMessage.objects.create(
            title='Общо съобщение',
            message='Системата ще бъде в профилактика в неделя.',
            target_role=BroadcastMessage.AUDIENCE_ALL,
            created_by=self.admin
        )

    def test_unread_filtering_by_role(self):
        client_teacher = APIClient()
        client_teacher.force_authenticate(user=self.teacher)

        resp_teacher = client_teacher.get('/api/broadcast-messages/unread/')
        self.assertEqual(resp_teacher.status_code, status.HTTP_200_OK)
        teacher_msg_ids = [m['id'] for m in resp_teacher.data]
        self.assertIn(self.msg_teacher.id, teacher_msg_ids)
        self.assertIn(self.msg_all.id, teacher_msg_ids)

        client_student = APIClient()
        client_student.force_authenticate(user=self.student)

        resp_student = client_student.get('/api/broadcast-messages/unread/')
        self.assertEqual(resp_student.status_code, status.HTTP_200_OK)
        student_msg_ids = [m['id'] for m in resp_student.data]
        self.assertNotIn(self.msg_teacher.id, student_msg_ids)
        self.assertIn(self.msg_all.id, student_msg_ids)

    def test_mark_message_read(self):
        client_teacher = APIClient()
        client_teacher.force_authenticate(user=self.teacher)

        # Mark teacher message as read
        resp_mark = client_teacher.post(f'/api/broadcast-messages/{self.msg_teacher.id}/mark-read/')
        self.assertEqual(resp_mark.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_mark.data['status'], 'ok')

        # Check unread list now only contains msg_all
        resp_teacher_after = client_teacher.get('/api/broadcast-messages/unread/')
        self.assertEqual(resp_teacher_after.status_code, status.HTTP_200_OK)
        teacher_msg_ids = [m['id'] for m in resp_teacher_after.data]
        self.assertNotIn(self.msg_teacher.id, teacher_msg_ids)
        self.assertIn(self.msg_all.id, teacher_msg_ids)

        # Mark msg_all as read
        resp_mark_all = client_teacher.post(f'/api/broadcast-messages/{self.msg_all.id}/mark-read/')
        self.assertEqual(resp_mark_all.status_code, status.HTTP_200_OK)

        # Now unread list is completely empty for this teacher
        resp_teacher_empty = client_teacher.get('/api/broadcast-messages/unread/')
        self.assertEqual(resp_teacher_empty.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp_teacher_empty.data), 0)

        # But student still sees msg_all
        client_student = APIClient()
        client_student.force_authenticate(user=self.student)
        resp_student = client_student.get('/api/broadcast-messages/unread/')
        student_msg_ids = [m['id'] for m in resp_student.data]
        self.assertIn(self.msg_all.id, student_msg_ids)

    def test_admin_crud_broadcast(self):
        client_admin = APIClient()
        client_admin.force_authenticate(user=self.admin)

        # Create
        resp_create = client_admin.post('/api/broadcast-messages/', {
            'title': 'Ново съобщение за ученици',
            'message': 'Тестът ще се проведе на 15-ти.',
            'target_role': BroadcastMessage.AUDIENCE_STUDENT,
            'is_active': True
        })
        self.assertEqual(resp_create.status_code, status.HTTP_201_CREATED)
        new_msg_id = resp_create.data['id']

        # Update
        resp_update = client_admin.put(f'/api/broadcast-messages/{new_msg_id}/', {
            'title': 'Обновено съобщение за ученици',
            'message': 'Тестът се отлага за 20-ти.',
            'target_role': BroadcastMessage.AUDIENCE_STUDENT,
            'is_active': True
        })
        self.assertEqual(resp_update.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_update.data['title'], 'Обновено съобщение за ученици')

        # Delete
        resp_del = client_admin.delete(f'/api/broadcast-messages/{new_msg_id}/')
        self.assertEqual(resp_del.status_code, status.HTTP_204_NO_CONTENT)
