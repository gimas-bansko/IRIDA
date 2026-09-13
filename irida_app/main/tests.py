from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from main.models import Subject, Specialty, School, Session, SessionPoint, SessionAttachment, Unit, Topic


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
