from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, University, Order, Message


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ['id', 'name', 'country', 'abbreviation', 'description']


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class BookListSerializer(serializers.ModelSerializer):
    university_name = serializers.CharField(source='university.name', read_only=True)
    seller_name = serializers.CharField(source='seller.username', read_only=True)
    cover_url = serializers.SerializerMethodField()
    grade_display = serializers.CharField(source='get_grade_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    condition_display = serializers.CharField(source='get_condition_display', read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'price', 'cover_url',
            'university', 'university_name', 'category', 'category_display',
            'grade', 'grade_display', 'condition', 'condition_display',
            'seller', 'seller_name', 'is_sold', 'created_at',
        ]

    def get_cover_url(self, obj):
        request = self.context.get('request')
        if obj.cover and request:
            return request.build_absolute_uri(obj.cover.url)
        return None


class BookDetailSerializer(BookListSerializer):
    seller = SellerSerializer(read_only=True)

    class Meta(BookListSerializer.Meta):
        fields = BookListSerializer.Meta.fields + [
            'description', 'program', 'course', 'year_published',
        ]


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'title', 'author', 'price', 'description', 'cover',
            'university', 'category', 'program', 'grade', 'course',
            'condition', 'year_published',
        ]

    def create(self, validated_data):
        validated_data['seller'] = self.context['request'].user
        return super().create(validated_data)


class OrderSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    buyer_name = serializers.CharField(source='buyer.username', read_only=True)
    seller_name = serializers.CharField(source='seller.username', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'book', 'book_title', 'buyer', 'buyer_name',
            'seller', 'seller_name', 'status', 'message', 'created_at', 'updated_at',
        ]
        read_only_fields = ['buyer', 'seller', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['buyer'] = self.context['request'].user
        validated_data['seller'] = validated_data['book'].seller
        return super().create(validated_data)


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    receiver_name = serializers.CharField(source='receiver.username', read_only=True)

    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'sender_name', 'receiver', 'receiver_name',
            'book', 'text', 'created_at', 'is_read',
        ]
        read_only_fields = ['sender', 'created_at']

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)
