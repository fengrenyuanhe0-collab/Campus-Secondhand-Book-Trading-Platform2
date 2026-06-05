from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import University, College, Major, Book, Order


class BookModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='seller', password='pass123')
        self.uni = University.objects.create(name='Test University', abbreviation='TU')
        self.book = Book.objects.create(
            title='Test Book', author='Author', price=100.00,
            seller=self.user, university=self.uni,
        )

    def test_platform_fee_is_5_percent(self):
        self.assertAlmostEqual(self.book.platform_fee_amount, 5.0)

    def test_seller_receives_95_percent(self):
        self.assertAlmostEqual(self.book.seller_receives, 95.0)

    def test_free_book_has_no_fee(self):
        self.book.price = None
        self.assertEqual(self.book.platform_fee_amount, 0.0)

    def test_book_str(self):
        self.assertIn('Test Book', str(self.book))


class UniversityModelTest(TestCase):
    def test_featured_university_orders_first(self):
        University.objects.create(name='Regular', abbreviation='R')
        University.objects.create(name='Featured', abbreviation='F', is_featured=True)
        first = University.objects.first()
        self.assertEqual(first.name, 'Featured')


class AuthViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='alice', email='alice@test.com', password='pass123'
        )

    def test_login_with_correct_credentials(self):
        response = self.client.post(reverse('users:login'), {
            'username': 'alice', 'password': 'pass123'
        })
        self.assertRedirects(response, reverse('books:home'))

    def test_login_with_wrong_password(self):
        response = self.client.post(reverse('users:login'), {
            'username': 'alice', 'password': 'wrong'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_register_creates_user(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'abc123',
            'password2': 'abc123',
        })
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_logout_redirects(self):
        self.client.login(username='alice', password='pass123')
        response = self.client.post(reverse('users:logout'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class BookViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='bob', password='pass123')
        self.uni = University.objects.create(name='UrFU', abbreviation='UrFU', is_featured=True)
        self.book = Book.objects.create(
            title='Django for Beginners', author='William Vincent',
            price=25.00, seller=self.user, university=self.uni,
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse('books:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_defaults_to_featured_university(self):
        response = self.client.get(reverse('books:home'))
        self.assertContains(response, 'UrFU')

    def test_book_detail_page_loads(self):
        response = self.client.get(reverse('books:detail', args=[self.book.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django for Beginners')

    def test_sell_page_requires_login(self):
        response = self.client.get(reverse('books:create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])

    def test_logged_in_user_can_access_sell_page(self):
        self.client.login(username='bob', password='pass123')
        response = self.client.get(reverse('books:create'))
        self.assertEqual(response.status_code, 200)

    def test_search_returns_matching_books(self):
        response = self.client.get(reverse('books:home') + '?search=Django')
        self.assertContains(response, 'Django for Beginners')

    def test_sold_book_not_shown_on_home(self):
        self.book.is_sold = True
        self.book.save()
        response = self.client.get(
            reverse('books:home') + f'?university={self.uni.pk}'
        )
        self.assertNotContains(response, 'Django for Beginners')


class CartTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='carol', password='pass123')
        self.seller = User.objects.create_user(username='dave', password='pass123')
        self.book = Book.objects.create(
            title='Cart Book', author='Author', price=10.00, seller=self.seller
        )

    def test_add_to_cart_requires_login(self):
        response = self.client.post(reverse('books:cart_add', args=[self.book.pk]))
        self.assertEqual(response.status_code, 302)

    def test_add_to_cart_success(self):
        self.client.login(username='carol', password='pass123')
        self.client.post(reverse('books:cart_add', args=[self.book.pk]))
        cart = self.client.session.get('cart', [])
        self.assertIn(self.book.pk, cart)
