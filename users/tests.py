from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from books.models import University, College, Major
from .models import UserProfile


class UserProfileTest(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name='UrFU', abbreviation='UrFU', is_featured=True)
        self.college = College.objects.create(university=self.uni, name='Institute of IT')
        self.major = Major.objects.create(college=self.college, name='Software Engineering')
        self.user = User.objects.create_user(username='testuser', password='pass123')

    def test_profile_created_automatically(self):
        # UserProfile should be auto-created with the user
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())

    def test_profile_can_set_university(self):
        profile = self.user.profile
        profile.university = self.uni
        profile.college = self.college
        profile.major = self.major
        profile.save()
        profile.refresh_from_db()
        self.assertEqual(profile.university, self.uni)
        self.assertEqual(profile.major.name, 'Software Engineering')

    def test_profile_display_name_uses_username_when_no_full_name(self):
        profile = self.user.profile
        self.assertEqual(profile.display_name, 'testuser')

    def test_profile_display_name_uses_full_name_when_set(self):
        self.user.first_name = 'Ivan'
        self.user.last_name = 'Petrov'
        self.user.save()
        self.assertEqual(self.user.profile.display_name, 'Ivan Petrov')


class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='student', password='pass123')

    def test_profile_setup_requires_login(self):
        response = self.client.get(reverse('users:choose_profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_page_loads_when_logged_in(self):
        self.client.login(username='student', password='pass123')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
