"""
API изгледи за AI промптове (списък, създаване, редакция и изтриване).
"""
import logging

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from ..audit import log_audit_event
from ..models import AIPrompt
from ..permissions import is_admin_user
from ..serializers import AIPromptSerializer


class AIPromptListView(APIView):
    """
    GET /api/prompts/?page_key=<page_key>
    Връща промптовете за конкретната страница плюс общите ('general').
    Ако page_key не е подаден, връща всички промптове.
    """
    def get(self, request):
        page_key = request.query_params.get('page_key', '').strip()
        if page_key and page_key != 'general':
            qs = AIPrompt.objects.filter(page_key__in=[page_key, 'general'])
            prompts = list(qs)
            # Промптовете за текущата страница излизат първи, следвани от общите
            prompts.sort(key=lambda p: (0 if p.page_key == page_key else 1, p.order, p.title))
        elif page_key == 'general':
            prompts = list(AIPrompt.objects.filter(page_key='general').order_by('order', 'title'))
        else:
            prompts = list(AIPrompt.objects.all().order_by('page_key', 'order', 'title'))

        serializer = AIPromptSerializer(prompts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class AIPromptUpsertView(APIView):
    """
    POST /api/prompts/upsert/
    Създава или редактира промпт.
    Body: { id, title, page_key, prompt_text, instructions, order }
    """
    def post(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response({'detail': 'Необходима е автентикация.'}, status=status.HTTP_403_FORBIDDEN)

        prompt_id = request.data.get('id', 0) or 0
        try:
            prompt_id = int(prompt_id)
        except (TypeError, ValueError):
            return Response({'detail': 'Невалиден идентификатор.'}, status=status.HTTP_400_BAD_REQUEST)

        title = str(request.data.get('title', '')).strip()
        prompt_text = str(request.data.get('prompt_text', '')).strip()
        page_key = str(request.data.get('page_key', 'general')).strip() or 'general'
        instructions = str(request.data.get('instructions', '')).strip()
        order = request.data.get('order', 1)
        try:
            order = int(order)
        except (TypeError, ValueError):
            order = 1

        if not title:
            return Response({'detail': 'Заглавието е задължително.'}, status=status.HTTP_400_BAD_REQUEST)
        if not prompt_text:
            return Response({'detail': 'Текстът на промпта е задължителен.'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        if prompt_id > 0:
            prompt = get_object_or_404(AIPrompt, id=prompt_id)
            if prompt.is_system:
                log_audit_event(
                    request=request,
                    action="PERMISSION_DENIED",
                    target_model="AIPrompt",
                    target_id=prompt.id,
                    status="DENIED",
                    details=f"Unauthorized update attempt on system prompt '{prompt.title}'",
                    level=logging.WARNING,
                )
                return Response(
                    {'detail': 'Системните шаблони не могат да се променят от потребителите. Промяна е възможна само през административния панел на Django.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            is_author = (prompt.created_by_id == user.id)
            if not is_author and not is_admin_user(user):
                log_audit_event(
                    request=request,
                    action="PERMISSION_DENIED",
                    target_model="AIPrompt",
                    target_id=prompt.id,
                    status="DENIED",
                    details=f"Unauthorized update attempt on AIPrompt '{prompt.title}'",
                    level=logging.WARNING,
                )
                return Response(
                    {'detail': 'Нямате права за редакция на този промпт.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            prompt.title = title
            prompt.page_key = page_key
            prompt.prompt_text = prompt_text
            prompt.instructions = instructions
            prompt.order = order
            prompt.save()

            log_audit_event(
                request=request,
                action="UPDATE",
                target_model="AIPrompt",
                target_id=prompt.id,
                status="SUCCESS",
                details=f"Updated AI prompt '{prompt.title}'"
            )
            serializer = AIPromptSerializer(prompt, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            prompt = AIPrompt.objects.create(
                title=title,
                page_key=page_key,
                prompt_text=prompt_text,
                instructions=instructions,
                order=order,
                is_system=False,
                created_by=user
            )
            log_audit_event(
                request=request,
                action="CREATE",
                target_model="AIPrompt",
                target_id=prompt.id,
                status="SUCCESS",
                details=f"Created AI prompt '{prompt.title}'"
            )
            serializer = AIPromptSerializer(prompt, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def ai_prompt_delete(request, pk):
    """
    DELETE /api/prompts/<pk>/
    Изтрива промпт по ID.
    """
    if not request.user or not request.user.is_authenticated:
        return Response({'detail': 'Необходима е автентикация.'}, status=status.HTTP_403_FORBIDDEN)

    prompt = get_object_or_404(AIPrompt, id=pk)
    user = request.user

    # Защита на системни промптове
    if prompt.is_system:
        log_audit_event(
            request=request,
            action="PERMISSION_DENIED",
            target_model="AIPrompt",
            target_id=prompt.id,
            status="DENIED",
            details=f"Unauthorized delete attempt on system prompt '{prompt.title}'",
            level=logging.WARNING,
        )
        return Response(
            {'detail': 'Системните шаблони не могат да бъдат изтривани от потребители.'},
            status=status.HTTP_403_FORBIDDEN
        )

    is_author = (prompt.created_by_id == user.id)
    if not is_author and not is_admin_user(user):
        log_audit_event(
            request=request,
            action="PERMISSION_DENIED",
            target_model="AIPrompt",
            target_id=prompt.id,
            status="DENIED",
            details=f"Unauthorized delete attempt on AIPrompt '{prompt.title}'",
            level=logging.WARNING,
        )
        return Response(
            {'detail': 'Нямате ��рава за изтриване на този промпт.'},
            status=status.HTTP_403_FORBIDDEN
        )

    prompt_title = prompt.title
    prompt.delete()
    log_audit_event(
        request=request,
        action="DELETE",
        target_model="AIPrompt",
        target_id=pk,
        status="SUCCESS",
        details=f"Deleted AI prompt '{prompt_title}'"
    )
    return Response(status=status.HTTP_204_NO_CONTENT)
