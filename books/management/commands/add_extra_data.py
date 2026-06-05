"""
python manage.py add_extra_data
Adds books from diverse universities, advertisements, sponsors, and demo users.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from books.models import University, Book, Advertisement, Sponsor

EXTRA_BOOKS = [
    # MIT
    {
        'uni': 'Massachusetts Institute of Technology',
        'title': 'Introduction to Computation and Programming Using Python',
        'author': 'John V. Guttag',
        'price': 38.00, 'category': 'cs', 'condition': 'good',
        'college': 'Faculty of Computer Science and Information Technology',
        'program': 'Computer Science', 'grade': '1',
        'course': 'Introduction to Programming', 'year_published': 2021,
        'description': 'The definitive MIT intro to CS using Python. Clean copy, no writing.',
    },
    {
        'uni': 'Massachusetts Institute of Technology',
        'title': 'Introduction to Linear Algebra',
        'author': 'Gilbert Strang',
        'price': 42.00, 'category': 'math', 'condition': 'like_new',
        'college': 'Faculty of Natural Sciences',
        'program': 'Mathematics', 'grade': '2',
        'course': 'Linear Algebra', 'year_published': 2022,
        'description': 'Legendary MIT linear algebra textbook by Gilbert Strang. Like new.',
    },
    # Cambridge
    {
        'uni': 'University of Cambridge',
        'title': 'The Art of Writing Reasonable Organic Reaction Mechanisms',
        'author': 'Robert B. Grossman',
        'price': 35.00, 'category': 'natural', 'condition': 'good',
        'college': 'Faculty of Natural Sciences',
        'program': 'Chemistry', 'grade': '3',
        'course': 'Organic Chemistry', 'year_published': 2020,
        'description': 'Excellent Cambridge chemistry text. Some highlighting in chapters 1-3.',
    },
    {
        'uni': 'University of Cambridge',
        'title': 'Politics and International Relations: An Introduction',
        'author': 'John Baylis',
        'price': 22.00, 'category': 'social', 'condition': 'good',
        'college': 'Faculty of Social Sciences',
        'program': 'International Relations', 'grade': '1',
        'course': 'Introduction to IR', 'year_published': 2021,
        'description': 'Cambridge intro to politics and IR. Very clean, used one semester.',
    },
    # Moscow State University
    {
        'uni': 'Moscow State University',
        'title': 'Mathematical Analysis',
        'author': 'Vladimir Zorich',
        'price': 28.00, 'category': 'math', 'condition': 'good',
        'college': 'Faculty of Natural Sciences',
        'program': 'Mathematics', 'grade': '1',
        'course': 'Mathematical Analysis I', 'year_published': 2019,
        'description': 'Classic Russian analysis textbook. Russian edition. Pencil notes only.',
    },
    {
        'uni': 'Moscow State University',
        'title': 'Theory of Probability and Mathematical Statistics',
        'author': 'Boris Gnedenko',
        'price': 20.00, 'category': 'math', 'condition': 'used',
        'college': 'Faculty of Natural Sciences',
        'program': 'Applied Mathematics', 'grade': '3',
        'course': 'Probability Theory', 'year_published': 2018,
        'description': 'Well-used but complete. Classic Soviet-era statistics textbook.',
    },
    # NUS
    {
        'uni': 'National University of Singapore',
        'title': 'Business Analytics: Data Analysis & Decision Making',
        'author': 'S. Christian Albright',
        'price': 45.00, 'category': 'business', 'condition': 'like_new',
        'college': 'Faculty of Economics and Business',
        'program': 'Business Administration', 'grade': '3',
        'course': 'Business Analytics', 'year_published': 2022,
        'description': 'NUS MBA-level analytics text. Barely used. Includes access code.',
    },
    {
        'uni': 'National University of Singapore',
        'title': 'Artificial Intelligence: A Modern Approach',
        'author': 'Stuart Russell',
        'price': 55.00, 'category': 'cs', 'condition': 'good',
        'college': 'Faculty of Computer Science and Information Technology',
        'program': 'Artificial Intelligence', 'grade': '4',
        'course': 'Artificial Intelligence', 'year_published': 2020,
        'description': 'The standard AI textbook worldwide. 4th edition. Some sticky notes.',
    },
    # Oxford
    {
        'uni': 'University of Oxford',
        'title': 'Economics',
        'author': 'Paul Samuelson',
        'price': 30.00, 'category': 'business', 'condition': 'good',
        'college': 'Faculty of Economics and Business',
        'program': 'Economics', 'grade': '1',
        'course': 'Principles of Economics', 'year_published': 2020,
        'description': 'Intro economics for Oxford students. Yellow highlighted key sections.',
    },
    {
        'uni': 'University of Oxford',
        'title': 'A Brief History of Time',
        'author': 'Stephen Hawking',
        'price': None, 'category': 'natural', 'condition': 'good',
        'college': 'Faculty of Natural Sciences',
        'program': 'Physics', 'grade': '1',
        'course': 'Modern Physics', 'year_published': 2017,
        'description': 'Free! Classic Hawking. Good condition, perfect for physics students.',
    },
    # Tsinghua
    {
        'uni': 'Tsinghua University',
        'title': 'C++ Primer',
        'author': 'Stanley B. Lippman',
        'price': 32.00, 'category': 'cs', 'condition': 'good',
        'college': 'Faculty of Computer Science and Information Technology',
        'program': 'Computer Science', 'grade': '2',
        'course': 'Object-Oriented Programming', 'year_published': 2013,
        'description': 'The definitive C++ reference. Chinese edition. Minor pencil marks.',
    },
    {
        'uni': 'Tsinghua University',
        'title': 'Data Structures and Algorithm Analysis in C',
        'author': 'Mark Allen Weiss',
        'price': 25.00, 'category': 'cs', 'condition': 'used',
        'college': 'Faculty of Computer Science and Information Technology',
        'program': 'Software Engineering', 'grade': '2',
        'course': 'Data Structures', 'year_published': 2014,
        'description': 'Widely used at Tsinghua CS. Some wear on cover but content intact.',
    },
    # ETH Zurich
    {
        'uni': 'ETH Zurich',
        'title': 'Numerical Methods for Engineers',
        'author': 'Steven Chapra',
        'price': 48.00, 'category': 'engineering', 'condition': 'like_new',
        'college': 'Faculty of Engineering',
        'program': 'Mechanical Engineering', 'grade': '3',
        'course': 'Numerical Methods', 'year_published': 2021,
        'description': 'ETH numerical methods. Bought but switched courses. Essentially new.',
    },
    # Harvard
    {
        'uni': 'Harvard University',
        'title': 'Justice: What\'s the Right Thing to Do?',
        'author': 'Michael Sandel',
        'price': 18.00, 'category': 'social', 'condition': 'good',
        'college': 'Faculty of Social Sciences',
        'program': 'Political Science', 'grade': '2',
        'course': 'Political Philosophy', 'year_published': 2010,
        'description': 'Based on Harvard\'s most popular course. Great condition, no writing.',
    },
    {
        'uni': 'Harvard University',
        'title': 'The Innovator\'s Dilemma',
        'author': 'Clayton Christensen',
        'price': 20.00, 'category': 'business', 'condition': 'good',
        'college': 'Faculty of Economics and Business',
        'program': 'Business Administration', 'grade': '3',
        'course': 'Innovation Management', 'year_published': 2016,
        'description': 'Harvard Business School classic. Light pen marks in introduction only.',
    },
    # Peking University
    {
        'uni': 'Peking University',
        'title': 'Compiler Principles',
        'author': 'Alfred V. Aho',
        'price': 35.00, 'category': 'cs', 'condition': 'good',
        'college': 'Faculty of Computer Science and Information Technology',
        'program': 'Computer Science', 'grade': '3',
        'course': 'Compiler Design', 'year_published': 2009,
        'description': 'The "Dragon Book" — essential for CS students. Chinese edition, clean.',
    },
    # Tokyo University
    {
        'uni': 'University of Tokyo',
        'title': 'Introduction to Robotics: Mechanics and Control',
        'author': 'John J. Craig',
        'price': 40.00, 'category': 'engineering', 'condition': 'like_new',
        'college': 'Faculty of Engineering',
        'program': 'Computer Engineering', 'grade': '4',
        'course': 'Robotics', 'year_published': 2018,
        'description': 'UTokyo robotics course textbook. English edition. Excellent condition.',
    },
    # UrFU extra books (different programs)
    {
        'uni': 'Ural Federal University',
        'title': 'Structural Analysis',
        'author': 'R.C. Hibbeler',
        'price': 33.00, 'category': 'engineering', 'condition': 'good',
        'college': 'Construction Institute',
        'program': 'Civil Engineering', 'grade': '3',
        'course': 'Structural Analysis', 'year_published': 2020,
        'description': 'UrFU civil engineering textbook. Some highlighting, great study resource.',
    },
    {
        'uni': 'Ural Federal University',
        'title': 'Electric Machinery Fundamentals',
        'author': 'Stephen J. Chapman',
        'price': 29.00, 'category': 'engineering', 'condition': 'good',
        'college': 'Ural Power Engineering Institute',
        'program': 'Electrical Engineering', 'grade': '3',
        'course': 'Electric Machinery', 'year_published': 2019,
        'description': 'Standard electrical engineering text at UrFU. Good reading copy.',
    },
    {
        'uni': 'Ural Federal University',
        'title': 'Marketing Management',
        'author': 'Philip Kotler',
        'price': 26.00, 'category': 'business', 'condition': 'like_new',
        'college': 'Graduate School of Economics and Management',
        'program': 'Marketing', 'grade': '2',
        'course': 'Marketing Management', 'year_published': 2022,
        'description': 'Kotler\'s classic. UrFU GSEM course book. Barely used, like new.',
    },
]

ADVERTISEMENTS = [
    {
        'title': 'Sell & Save: Textbook Exchange',
        'advertiser_name': 'Campus Books Platform',
        'link_url': '',
        'price_paid': 0,
        'position': 1,
        'is_active': True,
    },
    {
        'title': 'UrFU Student Discount — 20% Off Printing',
        'advertiser_name': 'UrFU Copy Center',
        'link_url': '',
        'price_paid': 150.00,
        'position': 2,
        'is_active': True,
    },
    {
        'title': 'Language Courses — English, German, Chinese',
        'advertiser_name': 'UrFU Language Institute',
        'link_url': '',
        'price_paid': 200.00,
        'position': 3,
        'is_active': True,
    },
    {
        'title': 'Student Housing — Rooms Near UrFU Campus',
        'advertiser_name': 'UrFU Housing Office',
        'link_url': '',
        'price_paid': 300.00,
        'position': 4,
        'is_active': False,
    },
]

SPONSORS = [
    {
        'name': 'UrFU Innovation Hub',
        'tier': 'gold',
        'donation_amount': 5000.00,
        'message': 'Supporting student entrepreneurship and knowledge exchange.',
        'website': '',
        'is_active': True,
    },
    {
        'name': 'Ural IT Park',
        'tier': 'silver',
        'donation_amount': 2500.00,
        'message': 'Connecting students with the regional tech ecosystem.',
        'website': '',
        'is_active': True,
    },
    {
        'name': 'Yekaterinburg Book Fair',
        'tier': 'bronze',
        'donation_amount': 1000.00,
        'message': 'Promoting reading culture among university students.',
        'website': '',
        'is_active': True,
    },
    {
        'name': 'Campus Coffee',
        'tier': 'donor',
        'donation_amount': 500.00,
        'message': 'Fueling students one cup at a time.',
        'website': '',
        'is_active': True,
    },
]

EXTRA_USERS = [
    ('ivan',    'ivan@urfu.ru',      'pass123', 'Ivan',    'Petrov'),
    ('maria',   'maria@urfu.ru',     'pass123', 'Maria',   'Sokolova'),
    ('dmitry',  'dmitry@mit.edu',    'pass123', 'Dmitry',  'Volkov'),
    ('sarah',   'sarah@cambridge.ac.uk', 'pass123', 'Sarah', 'Bennett'),
]


class Command(BaseCommand):
    help = 'Add diverse books from multiple universities, ads, sponsors, and users'

    def handle(self, *args, **options):
        uni_map = {u.name: u for u in University.objects.all()}

        # ── Extra users ───────────────────────────────────────────────────
        self.stdout.write('Adding extra users...')
        extra_users = []
        for username, email, password, first, last in EXTRA_USERS:
            if not User.objects.filter(username=username).exists():
                u = User.objects.create_user(username=username, email=email, password=password,
                                             first_name=first, last_name=last)
                self.stdout.write(f'  Created: {username}')
            extra_users.append(User.objects.get(username=username))

        all_sellers = list(User.objects.filter(username__in=['alice', 'bob', 'ivan', 'maria', 'dmitry', 'sarah']))
        if not all_sellers:
            all_sellers = list(User.objects.exclude(is_superuser=True)[:4])

        # ── Extra books ───────────────────────────────────────────────────
        self.stdout.write('Adding books from multiple universities...')
        added = 0
        for i, data in enumerate(EXTRA_BOOKS):
            uni = uni_map.get(data['uni'])
            if not uni:
                self.stdout.write(f'  Skip (no uni): {data["uni"]}')
                continue
            seller = all_sellers[i % len(all_sellers)]
            if Book.objects.filter(title=data['title']).exists():
                self.stdout.write(f'  Skip existing: {data["title"][:40]}')
                continue
            Book.objects.create(
                title=data['title'], author=data['author'],
                price=data.get('price'), description=data['description'],
                university=uni, college=data.get('college', ''),
                program=data.get('program', ''), grade=data['grade'],
                course=data['course'], condition=data['condition'],
                category=data['category'],
                year_published=data.get('year_published'),
                seller=seller,
            )
            self.stdout.write(f'  Book: {data["title"][:45]} [{uni.abbreviation}]')
            added += 1

        # ── Advertisements ────────────────────────────────────────────────
        self.stdout.write('Adding advertisements...')
        for ad_data in ADVERTISEMENTS:
            if not Advertisement.objects.filter(title=ad_data['title']).exists():
                Advertisement.objects.create(**ad_data)
                self.stdout.write(f'  Ad: {ad_data["title"]}')

        # ── Sponsors ──────────────────────────────────────────────────────
        self.stdout.write('Adding sponsors...')
        for sp_data in SPONSORS:
            if not Sponsor.objects.filter(name=sp_data['name']).exists():
                Sponsor.objects.create(**sp_data)
                self.stdout.write(f'  Sponsor: {sp_data["name"]} ({sp_data["tier"]})')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! +{added} books, {len(ADVERTISEMENTS)} ads, {len(SPONSORS)} sponsors'
        ))
