"""
books/urls.py
URL routing for books app / 书籍应用路由
"""
from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    # 主页 / Home page
    path('home/', views.home, name='home'),

    # 书籍详情 / Book detail
    path('book/<int:pk>/', views.book_detail, name='detail'),

    # 书籍增删改 / Book CRUD
    path('book/new/', views.create_book, name='create'),
    path('book/<int:pk>/edit/', views.edit_book, name='edit'),
    path('book/<int:pk>/delete/', views.delete_book, name='delete'),

    # 购物车 / Shopping cart
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='cart_add'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='cart_remove'),
    path('cart/clear/', views.clear_cart, name='cart_clear'),

    # 站内聊天 / In-platform chat
    path('chat/', views.chat_view, name='chat'),
    path('chat/<int:user_id>/', views.chat_view, name='chat_user'),
    path('chat/<int:user_id>/poll/', views.api_messages_poll, name='chat_poll'),

    # 结账与订单 / Checkout and orders
    path('checkout/', views.checkout_view, name='checkout'),
    path('orders/', views.orders_view, name='orders'),

    # 标记已售 / Mark as sold
    path('book/<int:pk>/mark-sold/', views.mark_sold, name='mark_sold'),

    # AJAX 级联下拉 / AJAX cascading dropdowns
    path('ajax/colleges/', views.api_colleges, name='ajax_colleges'),
    path('ajax/majors/', views.api_majors, name='ajax_majors'),
]
