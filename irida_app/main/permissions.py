"""
Класове за права за достъп (DRF Permissions) и помощни функции за авторство.
"""

from rest_framework import permissions

from .audit import log_audit_event
from .constants import SUPERADMIN, GUESTADMIN, SCHOOLADMIN, TEACHER, STUDENT


def is_admin_user(user):
    if not user or not getattr(user, 'is_authenticated', False):
        return False
    if getattr(user, 'is_superuser', False):
        return True
    user_profile = getattr(user, 'userprofile', None)
    role = getattr(user_profile, 'access_level', None)
    return role in [SUPERADMIN, GUESTADMIN, SCHOOLADMIN]


def get_object_author(obj):
    if hasattr(obj, 'author'):
        return obj.author
    if hasattr(obj, 'creator'):
        return obj.creator
    if hasattr(obj, 'created_by'):
        return obj.created_by
    return None


def get_object_author_id(obj):
    if hasattr(obj, 'author_id'):
        return obj.author_id
    if hasattr(obj, 'creator_id'):
        return obj.creator_id
    if hasattr(obj, 'created_by_id'):
        return obj.created_by_id
    return None


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешава четене за всички аутентикирани потребители.
    Редакция и изтриване се разрешават само за автора или администратор.
    За анонимно/неавторско съдържание (author is None):
      - Редакция е разрешена за аутентикирани потребители (при редакция става авторско).
      - Изтриване е разрешено само за администратори.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user or not request.user.is_authenticated:
            return False
        if is_admin_user(request.user):
            return True

        author_id = get_object_author_id(obj)
        if author_id is not None:
            return author_id == request.user.id

        # При липсващ автор (author is None)
        if request.method == 'DELETE':
            return False
        return True


def handle_author_on_save(instance, request, is_create=False):
    """
    Управлява авторството при запис:
    - При create: ако не е зададен author, се задава request.user (или session.author).
    - При update:
      - Ако instance.author е None -> задава се request.user.
      - Ако потребителят е администратор:
        - claim_ownership=True -> задава се request.user.
        - 'author' в request.data -> задава се подадения author_id.
        - keep_original_author=True (по подразбиране за админи) -> запазва се оригиналния автор.
    """
    if not request or not getattr(request, 'user', None) or not request.user.is_authenticated:
        return

    user = request.user
    is_admin = is_admin_user(user)

    if is_create:
        current_author_id = get_object_author_id(instance)
        if current_author_id is None:
            if hasattr(instance, 'author_id'):
                instance.author = user
            elif hasattr(instance, 'creator_id'):
                instance.creator = user
            elif hasattr(instance, 'created_by_id'):
                instance.created_by = user
    else:
        current_author_id = get_object_author_id(instance)
        if current_author_id is None:
            # Автоматично придобива авторство при първа редакция
            if hasattr(instance, 'author_id'):
                instance.author = user
            elif hasattr(instance, 'creator_id'):
                instance.creator = user
            elif hasattr(instance, 'created_by_id'):
                instance.created_by = user
        elif is_admin:
            claim_val = request.data.get('claim_ownership')
            claim_ownership = (claim_val is True) or (str(claim_val).strip().lower() in ('true', '1', 'yes', 't'))
            if claim_ownership:
                if hasattr(instance, 'author_id'):
                    instance.author = user
                elif hasattr(instance, 'creator_id'):
                    instance.creator = user
                elif hasattr(instance, 'created_by_id'):
                    instance.created_by = user
            elif 'author' in request.data:
                author_val = request.data.get('author')
                if author_val:
                    from django.contrib.auth.models import User
                    try:
                        new_author = User.objects.get(id=author_val)
                        if hasattr(instance, 'author'):
                            instance.author = new_author
                    except User.DoesNotExist:
                        pass
