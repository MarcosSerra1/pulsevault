from django.urls import path
from .views import CustomUserCreateView, CustomUserListView, CustomUserRetriveUpdateDestroyView


urlpatterns = [
    path('users/register/', CustomUserCreateView.as_view(), name='user-create'),
    path('users/list/', CustomUserListView.as_view(), name='user-list'),
    path('users/<uuid:pk>/', CustomUserRetriveUpdateDestroyView.as_view(), name='user-detail-view'),
]
