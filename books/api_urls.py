from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import BookViewSet, UniversityViewSet, OrderViewSet, MessageViewSet, CurrentUserView

router = DefaultRouter()
router.register('books', BookViewSet, basename='api-book')
router.register('universities', UniversityViewSet, basename='api-university')
router.register('orders', OrderViewSet, basename='api-order')
router.register('messages', MessageViewSet, basename='api-message')

urlpatterns = [
    path('', include(router.urls)),
    path('users/me/', CurrentUserView.as_view(), name='api-me'),
]
