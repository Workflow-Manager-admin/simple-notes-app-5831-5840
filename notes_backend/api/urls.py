from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import health, NoteViewSet, UserRegistrationView, LoginView

router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')

urlpatterns = [
    path('health/', health, name='Health'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]

urlpatterns += router.urls
