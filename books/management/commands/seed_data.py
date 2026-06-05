"""
seed_data.py
Populates: Universities → Colleges → Majors, demo users, sample books.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from books.models import University, College, Major, Book


# ── UrFU: real institute / faculty structure ────────────────────────────────
URFU_COLLEGES = {
    'Institute of Humanities and Arts': [
        'Linguistics and Intercultural Communication',
        'History',
        'Philosophy',
        'Art History and Cultural Studies',
        'Russian Language and Literature',
        'Advertising and Public Relations',
        'Journalism',
    ],
    'Graduate School of Economics and Management': [
        'Management',
        'Finance and Credit',
        'Marketing',
        'Human Resource Management',
        'Business Informatics',
        'International Business',
    ],
    'Institute of Economics and Management': [
        'Economics',
        'State and Municipal Administration',
        'Trade Policy and Commerce',
        'Taxation and Tax Administration',
        'Regional and Municipal Economics',
    ],
    'Institute of Social and Political Sciences': [
        'Sociology',
        'Political Science',
        'Social Work',
        'Cultural Studies',
        'Conflict Studies',
    ],
    'Ural Humanitarian Institute': [
        'Psychology',
        'Pedagogy and Psychology',
        'Social and Cultural Service',
        'Religious Studies',
    ],
    'Institute of Radioelectronics and Information Technologies': [
        'Computer Science and Engineering',
        'Software Engineering',
        'Information Security',
        'Radio Engineering',
        'Telecommunications and Communication Systems',
        'Electronics and Nanoelectronics',
        'Applied Informatics',
    ],
    'Institute of Natural Sciences and Mathematics': [
        'Mathematics',
        'Applied Mathematics and Informatics',
        'Physics',
        'Chemistry',
        'Biology',
        'Ecology and Nature Management',
        'Geography',
    ],
    'Institute of Physics and Technology': [
        'Applied Physics and Mathematics',
        'Nuclear Energy and Industry',
        'Materials Science and Technology',
        'Laser Physics',
        'Technical Physics',
    ],
    'Mechanical Engineering Institute': [
        'Mechanical Engineering Technology',
        'Robotics and Mechatronics',
        'Automotive Engineering',
        'Aircraft Engineering',
        'Standardization and Metrology',
        'Industrial Engineering',
    ],
    'Metallurgy Institute': [
        'Metallurgy',
        'Materials Science',
        'Welding Engineering and Technology',
        'Metal Forming Technology',
    ],
    'Chemical Technology Institute': [
        'Chemical Technology',
        'Biotechnology',
        'Food Product Technology',
        'Environmental Protection Technology',
    ],
    'Construction Institute': [
        'Civil Engineering',
        'Architecture',
        'Urban Planning',
        'Heat Supply and Ventilation',
        'Real Estate Economics and Management',
    ],
    'Ural Power Engineering Institute': [
        'Electrical Engineering',
        'Power Engineering',
        'Heat and Power Engineering',
        'Energy and Resource Saving',
        'Industrial Automation',
    ],
    'Institute of Public Administration and Entrepreneurship': [
        'Law',
        'Public Administration',
        'Business Administration',
        'Municipal Government',
        'Customs Affairs',
    ],
    'Institute of International Relations': [
        'International Relations',
        'Regional Studies',
        'Translation and Interpreting',
        'Foreign Regional Studies',
        'International Economics',
    ],
}

# ── Generic template shared by non-UrFU universities ───────────────────────
GENERIC_COLLEGES = {
    'Faculty of Engineering': [
        'Civil Engineering',
        'Mechanical Engineering',
        'Electrical Engineering',
        'Computer Engineering',
        'Chemical Engineering',
        'Industrial Engineering',
    ],
    'Faculty of Computer Science and Information Technology': [
        'Computer Science',
        'Software Engineering',
        'Information Technology',
        'Data Science and Analytics',
        'Cybersecurity',
        'Artificial Intelligence',
    ],
    'Faculty of Economics and Business': [
        'Economics',
        'Business Administration',
        'Finance and Accounting',
        'Marketing',
        'Human Resource Management',
        'International Business',
    ],
    'Faculty of Natural Sciences': [
        'Mathematics',
        'Physics',
        'Chemistry',
        'Biology',
        'Applied Mathematics',
        'Environmental Science',
    ],
    'Faculty of Humanities': [
        'History',
        'Philosophy',
        'Literature and Linguistics',
        'Foreign Languages',
        'Art History',
        'Journalism',
    ],
    'Faculty of Social Sciences': [
        'Sociology',
        'Psychology',
        'Political Science',
        'Law',
        'Social Work',
        'International Relations',
    ],
}

# ── University list ─────────────────────────────────────────────────────────
# (name, country, abbr, is_featured, colleges_dict)
UNIVERSITIES = [
    ('Ural Federal University', 'Russia', 'UrFU', True, URFU_COLLEGES),
    # ── Other Russian universities ──
    ('Moscow State University', 'Russia', 'MSU', False, GENERIC_COLLEGES),
    ('Saint Petersburg State University', 'Russia', 'SPBU', False, GENERIC_COLLEGES),
    ('Novosibirsk State University', 'Russia', 'NSU', False, GENERIC_COLLEGES),
    # ── International universities ──
    ('Massachusetts Institute of Technology', 'USA', 'MIT', False, GENERIC_COLLEGES),
    ('Harvard University', 'USA', 'Harvard', False, GENERIC_COLLEGES),
    ('University of Cambridge', 'UK', 'Cambridge', False, GENERIC_COLLEGES),
    ('University of Oxford', 'UK', 'Oxford', False, GENERIC_COLLEGES),
    ('National University of Singapore', 'Singapore', 'NUS', False, GENERIC_COLLEGES),
    ('University of Tokyo', 'Japan', 'UTokyo', False, GENERIC_COLLEGES),
    ('Seoul National University', 'South Korea', 'SNU', False, GENERIC_COLLEGES),
    ('ETH Zurich', 'Switzerland', 'ETH', False, GENERIC_COLLEGES),
    ('Technical University of Munich', 'Germany', 'TUM', False, GENERIC_COLLEGES),
    ('University of Toronto', 'Canada', 'UofT', False, GENERIC_COLLEGES),
    # ── Chinese universities ──
    ('Peking University', 'China', 'PKU', False, GENERIC_COLLEGES),
    ('Tsinghua University', 'China', 'THU', False, GENERIC_COLLEGES),
    ('Fudan University', 'China', 'FDU', False, GENERIC_COLLEGES),
    ('Shanghai Jiao Tong University', 'China', 'SJTU', False, GENERIC_COLLEGES),
    ('Zhejiang University', 'China', 'ZJU', False, GENERIC_COLLEGES),
    ('Wuhan University', 'China', 'WHU', False, GENERIC_COLLEGES),
]

# ── Sample books (updated with UrFU colleges/programs) ──────────────────────
BOOKS = [
    {
        'title': 'Introduction to Algorithms',
        'author': 'Thomas H. Cormen',
        'price': 35.00,
        'description': 'Definitive textbook on algorithms. Covers sorting, searching, graph algorithms, and complexity. Slight pencil marks on first 50 pages, otherwise excellent.',
        'uni': 'Ural Federal University',
        'college': 'Institute of Radioelectronics and Information Technologies',
        'program': 'Software Engineering',
        'grade': '2',
        'course': 'Data Structures & Algorithms',
        'condition': 'good',
        'category': 'cs',
        'year_published': 2022,
    },
    {
        'title': 'Calculus: Early Transcendentals',
        'author': 'James Stewart',
        'price': 28.00,
        'description': 'Classic calculus textbook. Includes all problem solutions booklet. Like new condition.',
        'uni': 'Ural Federal University',
        'college': 'Institute of Natural Sciences and Mathematics',
        'program': 'Mathematics',
        'grade': '1',
        'course': 'Mathematical Analysis',
        'condition': 'like_new',
        'category': 'math',
        'year_published': 2021,
    },
    {
        'title': 'Principles of Economics',
        'author': 'N. Gregory Mankiw',
        'price': 22.00,
        'description': 'Introductory economics covering micro and macro theory with real-world examples. Some highlighting.',
        'uni': 'Ural Federal University',
        'college': 'Graduate School of Economics and Management',
        'program': 'Economics',
        'grade': '1',
        'course': 'Microeconomics',
        'condition': 'good',
        'category': 'business',
        'year_published': 2020,
    },
    {
        'title': 'Linear Algebra and Its Applications',
        'author': 'David C. Lay',
        'price': 24.00,
        'description': 'Widely-used linear algebra textbook. Focuses on applications in engineering and data science. Clean copy.',
        'uni': 'Ural Federal University',
        'college': 'Institute of Natural Sciences and Mathematics',
        'program': 'Applied Mathematics and Informatics',
        'grade': '2',
        'course': 'Linear Algebra',
        'condition': 'like_new',
        'category': 'math',
        'year_published': 2021,
    },
    {
        'title': 'Computer Networks: A Top-Down Approach',
        'author': 'James Kurose',
        'price': 30.00,
        'description': 'Comprehensive computer networking textbook. Covers TCP/IP, HTTP, routing and security.',
        'uni': 'Ural Federal University',
        'college': 'Institute of Radioelectronics and Information Technologies',
        'program': 'Computer Science and Engineering',
        'grade': '3',
        'course': 'Computer Networks',
        'condition': 'good',
        'category': 'cs',
        'year_published': 2021,
    },
    {
        'title': 'Organic Chemistry',
        'author': 'Paula Yurkanis Bruice',
        'price': 40.00,
        'description': 'Comprehensive organic chemistry text with chapter summaries and practice problems.',
        'uni': 'Ural Federal University',
        'college': 'Institute of Natural Sciences and Mathematics',
        'program': 'Chemistry',
        'grade': '2',
        'course': 'Organic Chemistry',
        'condition': 'good',
        'category': 'natural',
        'year_published': 2019,
    },
    {
        'title': 'Fundamentals of Database Systems',
        'author': 'Ramez Elmasri',
        'price': None,
        'description': 'Free giveaway! Covers SQL, normalization, and transactions. Coffee stain on cover but content is perfect.',
        'uni': 'Ural Federal University',
        'college': 'Institute of Radioelectronics and Information Technologies',
        'program': 'Software Engineering',
        'grade': '3',
        'course': 'Database Systems',
        'condition': 'used',
        'category': 'cs',
        'year_published': 2016,
    },
    {
        'title': 'Financial Accounting',
        'author': 'Jerry J. Weygandt',
        'price': 18.00,
        'description': 'Standard financial accounting text. Yellow highlighting in first 3 chapters only.',
        'uni': 'Ural Federal University',
        'college': 'Graduate School of Economics and Management',
        'program': 'Finance and Credit',
        'grade': '2',
        'course': 'Financial Accounting',
        'condition': 'good',
        'category': 'business',
        'year_published': 2020,
    },
    {
        'title': 'Introduction to International Relations',
        'author': 'Joshua Goldstein',
        'price': 20.00,
        'description': 'Clear and comprehensive intro to IR theory. Covers realism, liberalism, constructivism. Minimal annotations.',
        'uni': 'Ural Federal University',
        'college': 'Institute of International Relations',
        'program': 'International Relations',
        'grade': '1',
        'course': 'Introduction to International Relations',
        'condition': 'good',
        'category': 'social',
        'year_published': 2021,
    },
    {
        'title': 'Probability and Statistics for Engineers',
        'author': 'Jay L. Devore',
        'price': 20.00,
        'description': 'Statistics text for engineering applications. Covers distributions, hypothesis testing, regression.',
        'uni': 'Ural Federal University',
        'college': 'Mechanical Engineering Institute',
        'program': 'Industrial Engineering',
        'grade': '2',
        'course': 'Engineering Statistics',
        'condition': 'used',
        'category': 'math',
        'year_published': 2018,
    },
    {
        'title': 'Introduction to Psychology',
        'author': 'David G. Myers',
        'price': 15.00,
        'description': 'Classic intro psych textbook. Engaging writing style. Minimal highlighting.',
        'uni': 'Ural Federal University',
        'college': 'Ural Humanitarian Institute',
        'program': 'Psychology',
        'grade': '1',
        'course': 'General Psychology',
        'condition': 'good',
        'category': 'social',
        'year_published': 2020,
    },
    {
        'title': 'Engineering Mechanics: Dynamics',
        'author': 'R.C. Hibbeler',
        'price': 32.00,
        'description': 'Core engineering mechanics text. All practice problems uncompleted — great for studying.',
        'uni': 'Ural Federal University',
        'college': 'Mechanical Engineering Institute',
        'program': 'Mechanical Engineering Technology',
        'grade': '2',
        'course': 'Engineering Mechanics',
        'condition': 'like_new',
        'category': 'engineering',
        'year_published': 2021,
    },
    {
        'title': 'Russian History: From Kievan Rus to the Present',
        'author': 'Nicholas Riasanovsky',
        'price': 12.00,
        'description': 'Comprehensive survey of Russian history. Some pencil annotations in margins (helpful context!).',
        'uni': 'Ural Federal University',
        'college': 'Institute of Humanities and Arts',
        'program': 'History',
        'grade': '3',
        'course': 'Russian History',
        'condition': 'used',
        'category': 'arts',
        'year_published': 2017,
    },
    {
        'title': 'Modern Operating Systems',
        'author': 'Andrew S. Tanenbaum',
        'price': 38.00,
        'description': 'Authoritative OS textbook covering processes, memory, file systems, and security.',
        'uni': 'Ural Federal University',
        'college': 'Institute of Radioelectronics and Information Technologies',
        'program': 'Computer Science and Engineering',
        'grade': '3',
        'course': 'Operating Systems',
        'condition': 'good',
        'category': 'cs',
        'year_published': 2022,
    },
    {
        'title': 'Environmental Science: Earth as a Living Planet',
        'author': 'Daniel B. Botkin',
        'price': None,
        'description': 'Free! Covers ecology, climate, energy, sustainability. Slightly worn cover, content complete.',
        'uni': 'Ural Federal University',
        'college': 'Institute of Natural Sciences and Mathematics',
        'program': 'Ecology and Nature Management',
        'grade': '2',
        'course': 'Environmental Science',
        'condition': 'used',
        'category': 'natural',
        'year_published': 2018,
    },
]


class Command(BaseCommand):
    help = 'Seed universities (with colleges & majors), demo users, and books'

    def handle(self, *args, **options):
        self.stdout.write('=== Seeding universities, colleges, and majors ===')
        uni_map = {}
        college_map = {}

        for name, country, abbr, featured, colleges_dict in UNIVERSITIES:
            uni, created = University.objects.get_or_create(
                name=name,
                defaults={'country': country, 'abbreviation': abbr, 'is_featured': featured},
            )
            uni_map[name] = uni
            tag = ' [UrFU ★]' if featured else ''
            if created:
                self.stdout.write(f'  University: {abbr} — {name}{tag}')

            for college_name, majors in colleges_dict.items():
                col, _ = College.objects.get_or_create(university=uni, name=college_name)
                college_map[(name, college_name)] = col
                for major_name in majors:
                    Major.objects.get_or_create(college=col, name=major_name)

        self.stdout.write(self.style.SUCCESS(
            f'  Done: {University.objects.count()} universities, '
            f'{College.objects.count()} colleges, '
            f'{Major.objects.count()} majors'
        ))

        self.stdout.write('\n=== Creating demo users ===')
        urfu = uni_map.get('Ural Federal University')
        demo_accounts = [
            ('admin', 'admin@campus.edu', 'admin123456', True),
            ('alice', 'alice@campus.edu', 'password123', False),
            ('bob', 'bob@campus.edu', 'password123', False),
        ]
        users = []
        for username, email, password, is_staff in demo_accounts:
            if not User.objects.filter(username=username).exists():
                u = User.objects.create_user(username=username, email=email, password=password)
                u.is_staff = is_staff
                u.is_superuser = is_staff
                u.save()
                # set default university to UrFU
                if urfu and hasattr(u, 'profile'):
                    u.profile.university = urfu
                    u.profile.save()
                self.stdout.write(f'  Created: {username}')
            users.append(User.objects.get(username=username))

        alice, bob = users[1], users[2]

        self.stdout.write('\n=== Seeding sample books ===')
        sellers = [alice, bob] * 10
        for i, data in enumerate(BOOKS):
            seller = sellers[i % len(sellers)]
            if Book.objects.filter(title=data['title'], seller=seller).exists():
                self.stdout.write(f'  Skip: {data["title"]}')
                continue
            uni = uni_map.get(data['uni'])
            Book.objects.create(
                title=data['title'],
                author=data['author'],
                price=data.get('price'),
                description=data['description'],
                university=uni,
                college=data.get('college', ''),
                program=data.get('program', ''),
                grade=data.get('grade', ''),
                course=data.get('course', ''),
                condition=data.get('condition', 'good'),
                category=data.get('category', 'other'),
                year_published=data.get('year_published'),
                seller=seller,
            )
            self.stdout.write(f'  Book: {data["title"]}')

        self.stdout.write(self.style.SUCCESS('\nDone! Seed complete.'))
        self.stdout.write('  admin / admin123456  (superuser)')
        self.stdout.write('  alice / password123')
        self.stdout.write('  bob   / password123')
