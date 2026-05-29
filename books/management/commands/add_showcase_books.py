"""
Run: python manage.py add_showcase_books
Adds 10 showcase books from the demo images.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from books.models import University, Book

SHOWCASE_BOOKS = [
    {
        'title': 'Cosmic Wonders: A Journey Through Space',
        'author': 'Dr. Elena Carter',
        'price': 18.00,
        'description': 'Exploring Galaxies, Black Holes, and the Big Bang. A visually rich journey through the cosmos — from stellar nurseries to the edge of the observable universe. Perfect for astronomy and astrophysics students.',
        'uni': 'Peking University',
        'category': 'natural',
        'program': 'Astrophysics',
        'grade': '2',
        'course': 'Introduction to Astronomy',
        'condition': 'like_new',
        'year_published': 2023,
        'college': 'School of Physics',
    },
    {
        'title': 'The Silk Road: Echoes of Ancient Trade',
        'author': 'Professor Marcus Wei',
        'price': 14.00,
        'description': 'From Xi\'an to Constantinople — Stories of Commerce and Culture. Traces the ancient trade routes that connected East and West, weaving together history, archaeology, and cultural exchange across continents.',
        'uni': 'Fudan University',
        'category': 'arts',
        'program': 'History',
        'grade': '3',
        'course': 'World History',
        'condition': 'good',
        'year_published': 2022,
        'college': 'School of History',
    },
    {
        'title': "The Mind's Mirror: Understanding Self-Perception",
        'author': 'Dr. Sophia Kim',
        'price': 16.00,
        'description': 'How Thoughts Shape Identity and Relationships. An insightful exploration of cognitive psychology and social perception — why we see ourselves the way we do, and how that shapes every relationship we build.',
        'uni': 'Beijing Normal University',
        'category': 'social',
        'program': 'Psychology',
        'grade': '2',
        'course': 'Social Psychology',
        'condition': 'like_new',
        'year_published': 2022,
        'college': 'School of Psychology',
    },
    {
        'title': 'Questions Without Answers: Existentialism in Modern Life',
        'author': 'Professor Eleanor Barnes',
        'price': 12.00,
        'description': 'Kierkegaard, Sartre, and the Search for Meaning. Examines existentialist philosophy from its 19th-century roots to contemporary applications — a provocative guide to living authentically in an uncertain world.',
        'uni': 'Renmin University of China',
        'category': 'arts',
        'program': 'Philosophy',
        'grade': '3',
        'course': 'Modern Philosophy',
        'condition': 'good',
        'year_published': 2021,
        'college': 'School of Philosophy',
    },
    {
        'title': 'Our Changing Planet: Climate, Landscapes, and Human Impact',
        'author': 'Dr. Lisa Chen',
        'price': 20.00,
        'description': 'From Glaciers to Rainforests — A Visual Journey. A comprehensive visual and scientific exploration of Earth\'s changing ecosystems, climate systems, and the footprint of human civilization on the natural world.',
        'uni': 'Xiamen University',
        'category': 'natural',
        'program': 'Environmental Science',
        'grade': '2',
        'course': 'Environmental Science',
        'condition': 'like_new',
        'year_published': 2023,
        'college': 'School of Environment',
    },
    {
        'title': 'Harmony of the Spheres: Music and the Universe',
        'author': 'Maestro Antonio Rossi',
        'price': 15.00,
        'description': 'How Sound Shapes Culture, Math, and the Human Brain. Bridges music theory, mathematics, and neuroscience — exploring why music moves us, how sound builds civilizations, and the mathematical patterns underlying all harmony.',
        'uni': 'Central South University',
        'category': 'arts',
        'program': 'Music Theory',
        'grade': '2',
        'course': 'Music and Mathematics',
        'condition': 'good',
        'year_published': 2022,
        'college': 'School of Music',
    },
    {
        'title': 'Whispers in the Attic',
        'author': 'Emma Richardson',
        'price': 8.00,
        'description': 'A Novel of Family Secrets and Forgotten Memories. A beautifully crafted literary novel following three generations of a family as buried secrets surface through a collection of letters found in an attic. Moving, mysterious, and masterfully written.',
        'uni': 'Sichuan University',
        'category': 'arts',
        'program': 'Literature',
        'grade': '4',
        'course': 'Contemporary Fiction',
        'condition': 'like_new',
        'year_published': 2021,
        'college': 'School of Literature',
    },
    {
        'title': 'The Beauty of Numbers: Patterns in Nature and Art',
        'author': 'Dr. Raj Patel',
        'price': 22.00,
        'description': 'Fibonacci, Fractals, and the Language of the Universe. Reveals the hidden mathematical patterns in sunflowers, seashells, galaxies, and Renaissance paintings — a stunning exploration of where mathematics and beauty collide.',
        'uni': 'Tsinghua University',
        'category': 'math',
        'program': 'Mathematics',
        'grade': '3',
        'course': 'Mathematical Beauty',
        'condition': 'good',
        'year_published': 2023,
        'college': 'School of Mathematics',
    },
    {
        'title': "Life's Blueprint: DNA and the Code of Evolution",
        'author': 'Dr. James Wilson',
        'price': 25.00,
        'description': 'From Mendel\'s Peas to CRISPR Technology. Traces the history of genetics from early inheritance experiments to modern gene editing — essential reading for biology, medicine, and anyone fascinated by the molecular machinery of life.',
        'uni': 'Wuhan University',
        'category': 'natural',
        'program': 'Biology',
        'grade': '1',
        'course': 'Introduction to Genetics',
        'condition': 'like_new',
        'year_published': 2023,
        'college': 'School of Life Sciences',
    },
    {
        'title': "Van Gogh's Palette: Emotions in Color",
        'author': 'Clara Dubois',
        'price': 13.00,
        'description': 'The Story Behind the Brushstrokes and Bold Hues. Art historian Clara Dubois takes readers inside Van Gogh\'s tumultuous mind through his explosive use of color — analyzing his most iconic works alongside his letters and psychological history.',
        'uni': 'Nanjing University',
        'category': 'arts',
        'program': 'Art History',
        'grade': '3',
        'course': 'Impressionism and Post-Impressionism',
        'condition': 'like_new',
        'year_published': 2022,
        'college': 'School of Arts',
    },
]


class Command(BaseCommand):
    help = 'Add 10 showcase books to the database'

    def handle(self, *args, **options):
        # Use alice and bob as sellers, fall back to first superuser
        sellers = list(User.objects.filter(username__in=['alice', 'bob']))
        if not sellers:
            sellers = list(User.objects.filter(is_superuser=True)[:2])
        if not sellers:
            self.stdout.write(self.style.ERROR(
                'No users found. Run seed_data first: python manage.py seed_data'
            ))
            return

        uni_map = {u.name: u for u in University.objects.all()}
        added = 0

        for i, data in enumerate(SHOWCASE_BOOKS):
            seller = sellers[i % len(sellers)]
            if Book.objects.filter(title=data['title'], seller=seller).exists():
                self.stdout.write(f'  Skip existing: {data["title"]}')
                continue

            Book.objects.create(
                title=data['title'],
                author=data['author'],
                price=data.get('price'),
                description=data['description'],
                university=uni_map.get(data['uni']),
                college=data.get('college', ''),
                category=data['category'],
                program=data['program'],
                grade=data['grade'],
                course=data['course'],
                condition=data['condition'],
                year_published=data.get('year_published'),
                seller=seller,
            )
            self.stdout.write(f'  Added: {data["title"]}')
            added += 1

        self.stdout.write(self.style.SUCCESS(f'\nDone! Added {added} showcase books.'))
        if added > 0:
            self.stdout.write('Note: Cover images can be uploaded via Edit on each book listing.')
