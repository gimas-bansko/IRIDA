from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from main.constants import STUDENT, TEACHER
from main.models import (
    Goal,
    School,
    SchoolDayConfig,
    Session,
    SessionAttachment,
    SessionPoint,
    SessionTask,
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
        self.assertTrue(resp.data['file_url'].endswith('theory_doc.pdf') or 'theory_doc' in resp.data['file_url'])
        self.assertTrue(resp.data['file_name'].startswith('theory_doc') and resp.data['file_name'].endswith('.pdf'))

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
