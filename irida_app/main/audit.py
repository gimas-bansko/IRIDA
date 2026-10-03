"""
Модул за одит и сигурност (Audit Logging).
Записва структурирани логове за автентикация, права на достъп и CRUD операции
както във файлов логер (audit.log), така и в базата данни (Log модел).
"""

import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.views import exception_handler

from .constants import SUPERADMIN, GUESTADMIN, SCHOOLADMIN, TEACHER, STUDENT

logger = logging.getLogger('irida.audit')

ROLE_NAMES = {
    SUPERADMIN: 'SUPERADMIN',
    GUESTADMIN: 'GUESTADMIN',
    SCHOOLADMIN: 'SCHOOLADMIN',
    TEACHER: 'TEACHER',
    STUDENT: 'STUDENT',
}


def get_client_ip(request):
    """
    Извлича IP адреса на клиента от HTTP заявката.
    """
    if not request:
        return '-'
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '-')
    return ip or '-'


def get_user_info(request=None, user=None):
    """
    Връща tuple (user_str, role_str) за потребителя.
    """
    target_user = user
    if target_user is None and request and hasattr(request, 'user'):
        target_user = request.user

    if target_user and getattr(target_user, 'is_authenticated', False):
        user_str = f"{target_user.id}:{target_user.username}"
        role_id = None
        user_profile = getattr(target_user, 'userprofile', None)
        if user_profile and user_profile.access_level:
            role_id = user_profile.access_level
        elif getattr(target_user, 'is_superuser', False):
            role_id = SUPERADMIN
        role_str = ROLE_NAMES.get(role_id, f"ROLE_{role_id}" if role_id is not None else "UNKNOWN")
    else:
        username = getattr(target_user, 'username', None)
        user_str = f"-:{username}" if username else "-:anonymous"
        role_str = "ANONYMOUS"

    return user_str, role_str


def log_audit_event(
    request=None,
    action="ACTION",
    target_model="-",
    target_id="-",
    status="SUCCESS",
    details="",
    user=None,
    level=logging.INFO,
):
    """
    Записва структуриран одит лог запис:
    1. Във файлов логер 'irida.audit' (logs/audit.log).
       Формат: [YYYY-MM-DD HH:MM:SS] [LEVEL] [IP] [USER_ID:username] [ROLE] [ACTION] [TARGET_ENTITY:ID] [STATUS] [DETAILS]
    2. В таблицата с действия Log в базата данни (визуализира се в Django Admin).
    """
    ip = get_client_ip(request)
    user_str, role_str = get_user_info(request=request, user=user)

    target_entity_str = f"{target_model}:{target_id if target_id is not None else '-'}"
    details_str = str(details) if details else "-"

    level_name = logging.getLevelName(level)
    msg = f"[{level_name}] [{ip}] [{user_str}] [{role_str}] [{action}] [{target_entity_str}] [{status}] [{details_str}]"

    if level == logging.ERROR:
        logger.error(msg)
    elif level == logging.WARNING:
        logger.warning(msg)
    else:
        logger.info(msg)

    # Запис в базата данни (Log модел)
    try:
        from .models.accounts import Log
        target_user = user
        if target_user is None and request and hasattr(request, 'user'):
            target_user = request.user

        u_id = 0
        u_name = 'anonymous'
        if target_user and getattr(target_user, 'is_authenticated', False):
            u_id = getattr(target_user, 'id', 0) or 0
            u_name = getattr(target_user, 'username', '') or ''
        elif target_user and getattr(target_user, 'username', None):
            u_name = target_user.username
        elif user_str and user_str.startswith("-:"):
            u_name = user_str[2:]

        action_entry = f"[{action}] [{target_entity_str}] [{status}] {details_str}"[:200]
        Log.objects.create(
            user_id=u_id,
            user_name=(u_name or 'anonymous')[:50],
            action=action_entry,
            date=timezone.now(),
        )
    except Exception as e:
        logger.debug("Failed to create DB Log record: %s", e)


def audit_exception_handler(exc, context):
    """
    DRF Exception Handler, който прихваща 403 Forbidden и записва събитие в одит лога.
    """
    response = exception_handler(exc, context)
    if response is not None and response.status_code == 403:
        request = context.get('request')
        view = context.get('view')
        view_name = view.__class__.__name__ if view else 'APIView'
        kwargs = getattr(view, 'kwargs', {}) if view else {}
        target_id = kwargs.get('pk') or kwargs.get('id') or kwargs.get('session_id') or '-'

        log_audit_event(
            request=request,
            action="PERMISSION_DENIED",
            target_model=view_name,
            target_id=target_id,
            status="DENIED",
            details=str(exc),
            level=logging.WARNING,
        )
    return response


# ******************************************************************************
#                     Сигнали за автентикация (Auth Signals)
# ******************************************************************************
@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    if getattr(request, '_audit_logged_in', False):
        return
    if request:
        request._audit_logged_in = True
    log_audit_event(
        request=request,
        action="LOGIN",
        target_model="User",
        target_id=user.id,
        status="SUCCESS",
        details=f"User '{user.username}' logged in successfully",
        user=user,
    )


@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    if getattr(request, '_audit_logged_out', False):
        return
    if request:
        request._audit_logged_out = True
    if user:
        log_audit_event(
            request=request,
            action="LOGOUT",
            target_model="User",
            target_id=user.id,
            status="SUCCESS",
            details=f"User '{user.username}' logged out",
            user=user,
        )


@receiver(user_login_failed)
def on_user_login_failed(sender, credentials, request, **kwargs):
    if getattr(request, '_audit_login_failed', False):
        return
    if request:
        request._audit_login_failed = True
    username = credentials.get('username', '') if credentials else ''
    log_audit_event(
        request=request,
        action="LOGIN_FAILED",
        target_model="User",
        target_id=username or '-',
        status="FAILED",
        details=f"Failed login attempt for username '{username}'",
        level=logging.WARNING,
    )
