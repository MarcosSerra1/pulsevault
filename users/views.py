from rest_framework import generics
from rest_framework.throttling import AnonRateThrottle
from django.http import JsonResponse
from .models import CustomUser
from .serializers import CustomUserSerializer, ListUserSerializer


# CustomThrottle é uma classe de limitação de taxa personalizada
class CustomThrottle(AnonRateThrottle):
    scope = 'create_user'  # Define o escopo para a limitação de taxa


class CustomUserCreateView(generics.CreateAPIView):
    throttle_classes = [CustomThrottle]  # Limita a criação de usuários
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CustomUserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ListUserSerializer


class CustomUserRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def delete(self, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
            return JsonResponse({'message': 'Usuário deletado com sucesso.'}, status=204)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
