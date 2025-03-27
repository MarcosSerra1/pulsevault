from django.urls import path
from .views import CustomUserCreateListView, CustomUserRetriveUpdateDestroyView


urlpatterns = [
    path('users/', CustomUserCreateListView.as_view(), name='user-create-list'),
    path('user/<int:pk>/', CustomUserRetriveUpdateDestroyView.as_view(), name='user-detail-view'),
]
