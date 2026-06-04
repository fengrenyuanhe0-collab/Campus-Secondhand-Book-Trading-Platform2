import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import RegisterForm, ProfileForm
from .models import UserProfile
from books.models import Book, University

logger = logging.getLogger('users')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('books:home')

    next_url = request.GET.get('next', request.POST.get('next', 'books:home'))

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Allow login by email
        if '@' in username:
            try:
                user_obj = User.objects.get(email=username)
                username = user_obj.username
            except User.DoesNotExist:
                pass

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            logger.info('User logged in: %s', user.username)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect(next_url if next_url and next_url != 'books:home' else 'books:home')
        else:
            messages.error(request, 'Invalid username/email or password.')
            logger.warning('Failed login attempt for: %s', username)

    return render(request, 'login.html', {'next': next_url})


def logout_view(request):
    if request.method == 'POST':
        username = request.user.username
        logout(request)
        logger.info('User logged out: %s', username)
        messages.success(request, 'You have been logged out.')
    return redirect('index')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('books:home')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
        )
        login(request, user)
        logger.info('New user registered: %s', user.username)
        messages.success(request, f'Account created! Welcome, {user.username}. Complete your profile.')
        return redirect('users:choose_profile')

    return render(request, 'register.html', {'form': form})


@login_required
def choose_profile(request):
    profile = request.user.profile
    form = ProfileForm(request.POST or None, instance=profile)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile updated!')
        return redirect('books:home')

    # Default university = UrFU (is_featured=True); fallback to profile's current value
    urfu = University.objects.filter(is_featured=True).first()
    default_uni_id = profile.university_id or (urfu.pk if urfu else None)

    # Pre-select UrFU if profile has no university set yet
    if not profile.university_id and urfu:
        profile.university = urfu

    universities = University.objects.all()

    return render(request, 'choose_profile.html', {
        'form': form,
        'universities': universities,
        'current_university_id': default_uni_id,
        'saved_college_id': profile.college_id or '',
        'saved_major_id': profile.major_id or '',
    })


@login_required
def profile_view(request):
    profile = request.user.profile
    form = ProfileForm(request.POST or None, instance=profile)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('users:profile')

    my_books = Book.objects.filter(seller=request.user).order_by('-created_at')
    return render(request, 'profile.html', {
        'profile': profile,
        'form': form,
        'my_books': my_books,
    })
