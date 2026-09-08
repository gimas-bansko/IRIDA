"""
Качване на картинки от WYSIWYG редакторите в съдържанието на урок.

Двата endpoint-а правят едно и също, различават се само по формата на
отговора, който съответният редактор очаква.
"""

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
@csrf_exempt  # вероятно без ефект - DRF/SessionAuthentication налага CSRF сама
def ckeditor_image_upload(request):
    """
    Expects: multipart/form-data with 'upload' field (CKEditor default)
    Returns: { "url": "<absolute-or-relative-url>" }
    """
    f = request.FILES.get('upload')
    if not f:
        return Response({'error': 'No file'}, status=400)

    # записваме файла
    # ВНИМАНИЕ: пази оригиналното име - файл със същото име се презаписва.
    # utils.session_image_upload_path() дава уникално име по timestamp.
    path = default_storage.save(f"session_pics/{f.name}", ContentFile(f.read()))
    url = default_storage.url(path)  # напр. /media/session_pics/...

    # CKEditor expects { url }
    return Response({'url': url}, status=201)


@api_view(['POST'])
@csrf_exempt  # вероятно без ефект - виж бележката по-горе
def tinymce_image_upload(request):
    """
    TinyMCE default handler expects:
        - multipart/form-data with 'file'
        - Response: { "location": "<absolute-or-relative-url>" }
    """

    f = request.FILES.get('file')
    if not f:
        return Response({'error': 'No file'}, status=400)

    # Запис на файл в MEDIA
    path = default_storage.save(f"session_pics/{f.name}", ContentFile(f.read()))
    url = default_storage.url(path)  # напр. /media/session_pics/...

    # Върни във формат, който TinyMCE очаква
    return Response({'location': url}, status=201)
