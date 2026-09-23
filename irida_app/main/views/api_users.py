"""
API за управление на потребители.
"""

from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import UserReadSerializer, UserSerializer


class UserListView(APIView):
    def get(self, request, sc, lvl):
        # Извличане на параметрите за филтриране от заявката
        school_id = sc
        level = lvl
        qs = User.objects.all().select_related('userprofile')
        if school_id and school_id != 0:
            qs = qs.filter(userprofile__school=school_id)
        if level:
            qs = qs.filter(userprofile__access_level__gte=level)
        # Сериализиране на резултатите
        serializer = UserReadSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserListCreateView(generics.ListCreateAPIView):
    """
    GET: (по избор) връща всички или филтрирани по query params:
        ?school=<id>&min_level=<n>&max_level=<m>
    POST: създава потребител {username, password?, email, first_name, last_name, userprofile{...}}
    """
    queryset = User.objects.all().select_related('userprofile').order_by('id')
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return UserReadSerializer if self.request.method == 'GET' else UserSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        school = self.request.query_params.get('school')
        min_level = self.request.query_params.get('min_level')
        max_level = self.request.query_params.get('max_level')

        if school:
            qs = qs.filter(userprofile__school=school)
        if min_level:
            qs = qs.filter(userprofile__access_level__gte=min_level)
        if max_level:
            qs = qs.filter(userprofile__access_level__lte=max_level)
        return qs


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all().select_related('userprofile')
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        # GET -> Read; PUT/PATCH -> Write; DELETE -> няма тяло
        return UserReadSerializer if self.request.method == 'GET' else UserSerializer
