from rest_framework import viewsets, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from django.contrib.auth.models import User

from .models import Book, University, Order, Message
from .serializers import (
    BookListSerializer, BookDetailSerializer, BookCreateSerializer,
    UniversitySerializer, OrderSerializer, MessageSerializer,
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        owner = getattr(obj, 'seller', getattr(obj, 'buyer', None))
        return owner == request.user


class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author', 'course', 'program']
    ordering_fields = ['created_at', 'price', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = Book.objects.filter(is_sold=False).select_related('seller', 'university')
        params = self.request.query_params
        if params.get('university'):
            qs = qs.filter(university_id=params['university'])
        if params.get('category'):
            qs = qs.filter(category=params['category'])
        if params.get('grade'):
            qs = qs.filter(grade=params['grade'])
        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return BookCreateSerializer
        return BookDetailSerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class UniversityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = [permissions.AllowAny]


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(Q(buyer=user) | Q(seller=user)).select_related('book', 'buyer', 'seller')

    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        serializer.save(buyer=self.request.user, seller=book.seller)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Message.objects.filter(Q(sender=user) | Q(receiver=user)).select_related('sender', 'receiver')
        other_id = self.request.query_params.get('with')
        if other_id:
            qs = qs.filter(Q(sender_id=other_id) | Q(receiver_id=other_id))
        return qs

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = getattr(user, 'profile', None)
        data = {
            'id': user.pk,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_joined': user.date_joined,
            'university': profile.university.name if profile and profile.university else None,
            'college': profile.college if profile else '',
            'major': profile.major if profile else '',
            'grade': profile.grade if profile else '',
        }
        return Response(data)
