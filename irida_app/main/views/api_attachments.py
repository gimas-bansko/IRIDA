"""
API за управление на глобални приложения / прикачени файлове към системата.
"""

import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..converters import convert_markdown_file
from ..models import AppAttachment
from ..serializers.attachments import AppAttachmentSerializer


class AppAttachmentListView(generics.ListAPIView):
    """
    GET /api/app-attachments/
    Връща списък с глобални приложения / файлове, сортирани по номер и id.
    Поддържа незадължителен query параметър ?filter=all|system|mine
    """
    serializer_class = AppAttachmentSerializer

    def get_queryset(self):
        qs = AppAttachment.objects.all().order_by('num', 'id')
        filter_type = self.request.query_params.get('filter', '').strip().lower()
        if filter_type == 'system':
            qs = qs.filter(is_system=True)
        elif filter_type == 'mine':
            if self.request.user.is_authenticated:
                qs = qs.filter(created_by=self.request.user)
            else:
                qs = qs.none()
        return qs


@api_view(['POST'])
@csrf_exempt
def app_attachment_upsert(request):
    """
    POST /api/app-attachments/upsert/
    POST body: { id, num, name, file, description, is_system, target_format }
    id == 0/missing -> create; id > 0 -> update
    """
    attachment_id = request.data.get('id', 0) or 0
    try:
        attachment_id = int(attachment_id)
    except (TypeError, ValueError):
        return Response({'detail': 'Невалидно ID'}, status=status.HTTP_400_BAD_REQUEST)

    data = request.data.dict() if hasattr(request.data, 'dict') else dict(request.data)
    target_format = (request.data.get('target_format') or '').strip().lower()

    if 'is_system' in data:
        is_sys_val = str(data.get('is_system', '')).lower() in ('true', '1', 'yes')
        data['is_system'] = is_sys_val

    # Проверка за качен файл и евентуално преобразуване от Markdown към docx / pdf
    uploaded_file = request.FILES.get('file')
    if uploaded_file and uploaded_file.name:
        fname_lower = uploaded_file.name.lower()
        if fname_lower.endswith(('.md', '.markdown')) and target_format in ('docx', 'pdf'):
            try:
                file_bytes = uploaded_file.read()
                out_bytes, new_filename, content_type = convert_markdown_file(
                    file_bytes, target_format, original_filename=uploaded_file.name
                )
                converted_file = SimpleUploadedFile(
                    name=new_filename,
                    content=out_bytes,
                    content_type=content_type
                )
                data['file'] = converted_file
                data['original_filename'] = new_filename

                # Актуализиране на наименованието на материала, ако е било със старо разширение или празно
                name_val = (data.get('name') or '').strip()
                if name_val.lower().endswith(('.md', '.markdown')):
                    base_n, _ = os.path.splitext(name_val)
                    data['name'] = f"{base_n}.{target_format}"
                elif not name_val:
                    data['name'] = new_filename
            except Exception as e:
                return Response(
                    {'detail': f'Грешка при конвертиране на Markdown файл: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            data['original_filename'] = uploaded_file.name
            name_val = (data.get('name') or '').strip()
            if not name_val:
                data['name'] = uploaded_file.name

    user = request.user if request.user.is_authenticated else None

    if attachment_id > 0:
        instance = get_object_or_404(AppAttachment, id=attachment_id)
        if user and not (user.is_staff or user.is_superuser) and instance.created_by != user:
            return Response(
                {'detail': 'Нямате права да променяте това приложение.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if 'file' not in request.FILES and ('file' not in data or not data['file']):
            data.pop('file', None)
            data.pop('original_filename', None)
        serializer = AppAttachmentSerializer(instance, data=data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        serializer = AppAttachmentSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def app_attachment_delete(request, pk):
    """
    DELETE /api/app-attachments/<pk>/
    Изтрива запис за глобално приложение / файл.
    """
    instance = get_object_or_404(AppAttachment, id=pk)
    user = request.user if request.user.is_authenticated else None
    if user and not (user.is_staff or user.is_superuser) and instance.created_by != user:
        return Response(
            {'detail': 'Нямате права да премахвате това приложение.'},
            status=status.HTTP_403_FORBIDDEN
        )
    instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
