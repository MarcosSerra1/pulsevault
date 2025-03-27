from django.urls import path
from .views import CustomUserCreateListView


urlpatterns = [
    path('users/', CustomUserCreateListView.as_view(), name='user-create-list'),
    # path('user/<int:pk>/', , name='user-detail-view'),
]
