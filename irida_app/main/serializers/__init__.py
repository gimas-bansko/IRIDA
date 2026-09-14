"""
DRF сериализатори, групирани по домейн - в същия ред на зависимости
като models/: curriculum -> schools -> lessons -> accounts.

Реекспортът пази `from main.serializers import SubjectSerializer`.
"""

from .accounts import (
    UserProfileExpandedSerializer,
    UserProfileSerializer,
    UserProfileSpecSerializer,
    UserReadSerializer,
    UserSerializer,
)
from .curriculum import (
    GoalSerializer,
    SubjectMiniSerializer,
    SubjectSerializer,
    TopicSerializer,
    TopicWriteSerializer,
    UnitSerializer,
    UnitWriteSerializer,
)
from .prompts import AIPromptSerializer
from .lessons import (
    SessionMiniSerializer,
    SessionNoteSerializer,
    SessionPointSerializer,
    SessionReadSerializer,
    SessionSerializer,
    SessionTaskSerializer,
    SessionAttachmentSerializer,
    SessionTopicReadSerializer,
    SessionTopicReadSerializerDetailed,
    SessionTopicWriteSerializer,
    SessionWriteSerializer,
)
from .schools import (
    SchoolDayConfigSerializer,
    SchoolLogoSerializer,
    SchoolMiniSerializer,
    SchoolSerializer,
    SchoolSerializer2,
    SpecialtyMiniSerializer,
    SpecialtySerializer,
)

__all__ = [
    # curriculum
    'SubjectSerializer',
    'SubjectMiniSerializer',
    'GoalSerializer',
    'TopicSerializer',
    'TopicWriteSerializer',
    'UnitSerializer',
    'UnitWriteSerializer',
    # prompts
    'AIPromptSerializer',
    # schools
    'SpecialtySerializer',
    'SpecialtyMiniSerializer',
    'SchoolSerializer',
    'SchoolSerializer2',
    'SchoolMiniSerializer',
    'SchoolLogoSerializer',
    'SchoolDayConfigSerializer',
    # lessons
    'SessionWriteSerializer',
    'SessionReadSerializer',
    'SessionSerializer',
    'SessionMiniSerializer',
    'SessionTopicWriteSerializer',
    'SessionTopicReadSerializer',
    'SessionTopicReadSerializerDetailed',
    'SessionPointSerializer',
    'SessionNoteSerializer',
    'SessionTaskSerializer',
    'SessionAttachmentSerializer',
    # accounts
    'UserSerializer',
    'UserReadSerializer',
    'UserProfileSerializer',
    'UserProfileSpecSerializer',
    'UserProfileExpandedSerializer',
]
