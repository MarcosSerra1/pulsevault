from rest_framework import generics
from django.http import JsonResponse
from .models import CustomUser
from .serializers import CustomUserSerializer


class CustomUserCreateListView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
