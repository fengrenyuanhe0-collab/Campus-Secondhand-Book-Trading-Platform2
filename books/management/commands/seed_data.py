"""
Run: python manage.py seed_data
Creates 20 universities, 3 demo users, and 15 books.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from books.models import University, Book


UNIVERSITIES = [
    ('Peking University', 'China', 'PKU'),
    ('Tsinghua University', 'China', 'THU'),
    ('Fudan University', 'China', 'FDU'),
    ('Shanghai Jiao Tong University', 'China', 'SJTU'),
    ('Zhejiang University', 'China', 'ZJU'),
    ('Nanjing University', 'China', 'NJU'),
    ('Wuhan University', 'China', 'WHU'),
    ('Sun Yat-sen University', 'China', 'SYSU'),
    ('Harbin Institute of Technology', 'China', 'HIT'),
    ('Xiamen University', 'China', 'XMU'),
    ('Tongji University', 'China', 'TONGJI'),
    ('Beijing Normal University', 'China', 'BNU'),
    ('Nankai University', 'China', 'NKU'),
    ('Sichuan University', 'China', 'SCU'),
    ('Huazhong University of Science and Technology', 'China', 'HUST'),
    ('Beijing Institute of Technology', 'China', 'BIT'),
    ('East China Normal University', 'China', 'ECNU'),
    ('Renmin University of China', 'China', 'RUC'),
    ('Central South University', 'China', 'CSU'),
    ('Jilin University', 'China', 'JLU'),
]

BOOKS = [
    {
        'title': 'Introduction to Algorithms',
        'author': 'Thomas H. Cormen',
        'price': 35.00,
        'description': 'The definitive textbook on algorithms. Covers sorting, searching, graph algorithms, and complexity. Essential for CS majors. Slight pencil marks on first 50 pages, otherwise excellent.',
        'uni': 'Tsinghua University',
        'category': 'cs',
        'program': 'Computer Science',
        'grade': '2',
        'course': 'Data Structures & Algorithms',
        'condition': 'good',
        'year_published': 2022,
    },
    {
        'title': 'Calculus: Early Transcendentals',
        'author': 'James Stewart',
        'price': 28.00,
        'description': 'Classic calculus textbook. Used across math and engineering programs. Includes all problem solutions booklet. Like new condition.',
        'uni': 'Peking University',
        'category': 'math',
        'program': 'Mathematics',
        'grade': '1',
        'course': 'Calculus I',
        'condition': 'like_new',
        'year_published': 2021,
    },
    {
        'title': 'Principles of Economics',
        'author': 'N. Gregory Mankiw',
        'price': 22.00,
        'description': 'Introductory economics by one of the leading economists. Covers micro and macro theory with real-world examples. Good condition with some highlighting.',
        'uni': 'Fudan University',
        'category': 'business',
        'program': 'Economics',
        'grade': '1',
        'course': 'Principles of Economics',
        'condition': 'good',
        'year_published': 2020,
    },
    {
        'title': 'Linear Algebra and Its Applications',
        'author': 'David C. Lay',
        'price': 24.00,
        'description': 'Widely-used linear algebra textbook. Focuses on applications in engineering and data science. Clean copy, no writing inside.',
        'uni': 'Shanghai Jiao Tong University',
        'category': 'math',
        'program': 'Applied Mathematics',
        'grade': '2',
        'course': 'Linear Algebra',
        'condition': 'like_new',
        'year_published': 2021,
    },
    {
        'title': 'Computer Networks: A Top-Down Approach',
        'author': 'James Kurose',
        'price': 30.00,
        'description': 'Comprehensive computer networking textbook. Covers TCP/IP, HTTP, DNS, routing and security. Some sticky note tabs but otherwise very clean.',
        'uni': 'Zhejiang University',
        'category': 'cs',
        'program': 'Computer Science',
        'grade': '3',
        'course': 'Computer Networks',
        'condition': 'good',
        'year_published': 2021,
    },
    {
        'title': 'Organic Chemistry',
        'author': 'Paula Yurkanis Bruice',
        'price': 40.00,
        'description': 'Comprehensive organic chemistry text. Includes chapter summaries and practice problems. Highly recommended. Perfect for pre-med students.',
        'uni': 'Wuhan University',
        'category': 'natural',
        'program': 'Chemistry',
        'grade': '2',
        'course': 'Organic Chemistry',
        'condition': 'good',
        'year_published': 2019,
    },
    {
        'title': 'Fundamentals of Database Systems',
        'author': 'Ramez Elmasri',
        'price': None,
        'description': 'Free giveaway! Moving out of dorm. Covers relational model, SQL, normalization, and transaction management. Some coffee stains on cover but content is perfect.',
        'uni': 'Nanjing University',
        'category': 'cs',
        'program': 'Software Engineering',
        'grade': '3',
        'course': 'Database Systems',
        'condition': 'used',
        'year_published': 2016,
    },
    {
        'title': 'Financial Accounting',
        'author': 'Jerry J. Weygandt',
        'price': 18.00,
        'description': 'Standard financial accounting text. Great for business majors and CPA exam prep. Clean with yellow highlighting in first 3 chapters.',
        'uni': 'Renmin University of China',
        'category': 'business',
        'program': 'Accounting',
        'grade': '2',
        'course': 'Financial Accounting',
        'condition': 'good',
        'year_published': 2020,
    },
    {
        'title': 'Human Anatomy & Physiology',
        'author': 'Elaine Marieb',
        'price': 45.00,
        'description': 'Comprehensive A&P textbook with atlas. Includes access code for online resources (unused). Perfect condition — barely used.',
        'uni': 'Sun Yat-sen University',
        'category': 'health',
        'program': 'Medicine',
        'grade': '1',
        'course': 'Anatomy & Physiology',
        'condition': 'like_new',
        'year_published': 2022,
    },
    {
        'title': 'Probability and Statistics for Engineers',
        'author': 'Jay L. Devore',
        'price': 20.00,
        'description': 'Statistics text tailored for engineering applications. Covers probability distributions, hypothesis testing, and regression. Used but in solid condition.',
        'uni': 'Harbin Institute of Technology',
        'category': 'math',
        'program': 'Engineering',
        'grade': '2',
        'course': 'Engineering Statistics',
        'condition': 'used',
        'year_published': 2018,
    },
    {
        'title': 'Introduction to Psychology',
        'author': 'David G. Myers',
        'price': 15.00,
        'description': 'Classic intro psych textbook, perfect for social science students. Engaging writing style. Minimal highlighting, good condition.',
        'uni': 'Beijing Normal University',
        'category': 'social',
        'program': 'Psychology',
        'grade': '1',
        'course': 'General Psychology',
        'condition': 'good',
        'year_published': 2020,
    },
    {
        'title': 'Engineering Mechanics: Dynamics',
        'author': 'R.C. Hibbeler',
        'price': 32.00,
        'description': 'Core engineering mechanics text. Covers kinematics, kinetics, work-energy methods. All practice problems are uncompleted — like new for studying.',
        'uni': 'Tongji University',
        'category': 'engineering',
        'program': 'Civil Engineering',
        'grade': '2',
        'course': 'Engineering Mechanics',
        'condition': 'like_new',
        'year_published': 2021,
    },
    {
        'title': 'Western Literature Anthology',
        'author': 'Various Authors',
        'price': 12.00,
        'description': 'Anthology covering major works from Homer to the 20th century. Required for Western Lit course. Some pencil annotations in margins (helpful!)',
        'uni': 'Sichuan University',
        'category': 'arts',
        'program': 'Literature',
        'grade': '3',
        'course': 'Western Literature',
        'condition': 'used',
        'year_published': 2017,
    },
    {
        'title': 'Modern Operating Systems',
        'author': 'Andrew S. Tanenbaum',
        'price': 38.00,
        'description': 'Authoritative OS textbook covering processes, memory management, file systems, and security. Excellent reference that goes beyond coursework.',
        'uni': 'Xiamen University',
        'category': 'cs',
        'program': 'Computer Science',
        'grade': '3',
        'course': 'Operating Systems',
        'condition': 'good',
        'year_published': 2022,
    },
    {
        'title': 'Environmental Science: Earth as a Living Planet',
        'author': 'Daniel B. Botkin',
        'price': None,
        'description': 'Free! Covers ecology, climate, energy, and sustainability. Great for anyone interested in environmental issues. Slightly worn cover, content is complete.',
        'uni': 'Jilin University',
        'category': 'natural',
        'program': 'Environmental Science',
        'grade': '2',
        'course': 'Environmental Science',
        'condition': 'used',
        'year_published': 2018,
    },
]


class Command(BaseCommand):
    help = 'Seed database with 20 universities, 3 demo users and 15 books'

    def handle(self, *args, **options):
        self.stdout.write('Seeding universities...')
        uni_map = {}
        for name, country, abbr in UNIVERSITIES:
            uni, created = University.objects.get_or_create(
                name=name,
                defaults={'country': country, 'abbreviation': abbr},
            )
            uni_map[name] = uni
            if created:
                self.stdout.write(f'  Created: {name}')

        self.stdout.write('Creating demo users...')
        users = []
        demo_accounts = [
            ('admin', 'admin@campus.edu', 'admin123456', True),
            ('alice', 'alice@campus.edu', 'password123', False),
            ('bob', 'bob@campus.edu', 'password123', False),
        ]
        for username, email, password, is_staff in demo_accounts:
            if not User.objects.filter(username=username).exists():
                u = User.objects.create_user(username=username, email=email, password=password)
                u.is_staff = is_staff
                u.is_superuser = is_staff
                u.save()
                self.stdout.write(f'  Created user: {username}')
            users.append(User.objects.get(username=username))

        alice, bob = users[1], users[2]

        self.stdout.write('Seeding books...')
        sellers = [alice, bob, alice, bob, alice, bob, alice, bob, alice, bob, alice, bob, alice, bob, alice]
        for i, data in enumerate(BOOKS):
            if Book.objects.filter(title=data['title'], seller=sellers[i]).exists():
                self.stdout.write(f'  Skip existing: {data["title"]}')
                continue
            Book.objects.create(
                title=data['title'],
                author=data['author'],
                price=data.get('price'),
                description=data['description'],
                university=uni_map.get(data['uni']),
                category=data['category'],
                program=data['program'],
                grade=data['grade'],
                course=data['course'],
                condition=data['condition'],
                year_published=data.get('year_published'),
                seller=sellers[i],
            )
            self.stdout.write(f'  Created book: {data["title"]}')

        self.stdout.write(self.style.SUCCESS('\nDone! Demo accounts:'))
        self.stdout.write('  admin / admin123456  (superuser)')
        self.stdout.write('  alice / password123')
        self.stdout.write('  bob   / password123')
