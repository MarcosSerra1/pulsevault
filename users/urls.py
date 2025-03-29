from django.urls import path
from .views import CustomUserCreateListView, CustomUserRetriveUpdateDestroyView


urlpatterns = [
    path('users/', CustomUserCreateListView.as_view(), name='users-create-list'),
    path('users/<uuid:pk>/', CustomUserRetriveUpdateDestroyView.as_view(), name='users-detail-view'),
]
