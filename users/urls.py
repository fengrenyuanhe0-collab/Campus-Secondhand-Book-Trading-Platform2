from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('login/',    views.login_view,    name='login'),
    path('logout/',   views.logout_view,   name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/',  views.profile_view,  name='profile'),
    path('profile/setup/', views.choose_profile, name='choose_profile'),

    # Password reset (Django built-in views)
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='password_reset/form.html',
             email_template_name='password_reset/email.html',
             subject_template_name='password_reset/subject.txt',
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset/done.html',
         ),
         name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset/confirm.html',
         ),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset/complete.html',
         ),
         name='password_reset_complete'),
]
