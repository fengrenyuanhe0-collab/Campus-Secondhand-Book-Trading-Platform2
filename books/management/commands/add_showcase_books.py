"""
Run: python manage.py add_showcase_books
Adds 10 showcase books, all assigned to Ural Federal University.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from books.models import University, Book

SHOWCASE_BOOKS = [
    {
        'title': 'Cosmic Wonders: A Journey Through Space',
        'author': 'Dr. Elena Carter',
        'price': 18.00,
        'description': 'Exploring Galaxies, Black Holes, and the Big Bang. A visually rich journey through the cosmos — from stellar nurseries to the edge of the observable universe.',
        'college': 'Institute of Natural Sciences and Mathematics',
        'program': 'Physics',
        'grade': '2',
        'course': 'Introduction to Astrophysics',
        'category': 'natural',
        'condition': 'like_new',
        'year_published': 2023,
    },
    {
        'title': 'The Silk Road: Echoes of Ancient Trade',
        'author': 'Professor Marcus Wei',
        'price': 14.00,
        'description': "From Xi'an to Constantinople — Stories of Commerce and Culture. Traces the ancient trade routes connecting East and West.",
        'college': 'Institute of Humanities and Arts',
        'program': 'History',
        'grade': '3',
        'course': 'World History',
        'category': 'arts',
        'condition': 'good',
        'year_published': 2022,
    },
    {
        'title': "The Mind's Mirror: Understanding Self-Perception",
        'author': 'Dr. Sophia Kim',
        'price': 16.00,
        'description': 'How Thoughts Shape Identity and Relationships. An insightful exploration of cognitive psychology and social perception.',
        'college': 'Ural Humanitarian Institute',
        'program': 'Psychology',
        'grade': '2',
        'course': 'Social Psychology',
        'category': 'social',
        'condition': 'like_new',
        'year_published': 2022,
    },
    {
        'title': 'Questions Without Answers: Existentialism in Modern Life',
        'author': 'Professor Eleanor Barnes',
        'price': 12.00,
        'description': 'Kierkegaard, Sartre, and the Search for Meaning. Examines existentialist philosophy from 19th-century roots to contemporary applications.',
        'college': 'Institute of Humanities and Arts',
        'program': 'Philosophy',
        'grade': '3',
        'course': 'Modern Philosophy',
        'category': 'arts',
        'condition': 'good',
        'year_published': 2021,
    },
    {
        'title': 'Our Changing Planet: Climate, Landscapes, and Human Impact',
        'author': 'Dr. Lisa Chen',
        'price': 20.00,
        'description': 'From Glaciers to Rainforests — A Visual Journey. Comprehensive exploration of Earth\'s changing ecosystems and climate systems.',
        'college': 'Institute of Natural Sciences and Mathematics',
        'program': 'Ecology and Nature Management',
        'grade': '2',
        'course': 'Environmental Science',
        'category': 'natural',
        'condition': 'like_new',
        'year_published': 2023,
    },
    {
        'title': 'Harmony of the Spheres: Music and the Universe',
        'author': 'Maestro Antonio Rossi',
        'price': 15.00,
        'description': 'How Sound Shapes Culture, Math, and the Human Brain. Bridges music theory, mathematics, and neuroscience.',
        'college': 'Institute of Natural Sciences and Mathematics',
        'program': 'Applied Mathematics and Informatics',
        'grade': '2',
        'course': 'Mathematics and Arts',
        'category': 'arts',
        'condition': 'good',
        'year_published': 2022,
    },
    {
        'title': 'Whispers in the Attic',
        'author': 'Emma Richardson',
        'price': 8.00,
        'description': 'A Novel of Family Secrets and Forgotten Memories. A beautifully crafted literary novel following three generations of a family.',
        'college': 'Institute of Humanities and Arts',
        'program': 'Russian Language and Literature',
        'grade': '4',
        'course': 'Contemporary Fiction',
        'category': 'arts',
        'condition': 'like_new',
        'year_published': 2021,
    },
    {
        'title': 'The Beauty of Numbers: Patterns in Nature and Art',
        'author': 'Dr. Raj Patel',
        'price': 22.00,
        'description': 'Fibonacci, Fractals, and the Language of the Universe. Hidden mathematical patterns in sunflowers, seashells, and galaxies.',
        'college': 'Institute of Natural Sciences and Mathematics',
        'program': 'Mathematics',
        'grade': '3',
        'course': 'Discrete Mathematics',
        'category': 'math',
        'condition': 'good',
        'year_published': 2023,
    },
    {
        'title': "Life's Blueprint: DNA and the Code of Evolution",
        'author': 'Dr. James Wilson',
        'price': 25.00,
        'description': "From Mendel's Peas to CRISPR Technology. Traces the history of genetics from early experiments to modern gene editing.",
        'college': 'Institute of Natural Sciences and Mathematics',
        'program': 'Biology',
        'grade': '1',
        'course': 'Introduction to Genetics',
        'category': 'natural',
        'condition': 'like_new',
        'year_published': 2023,
    },
    {
        'title': "Van Gogh's Palette: Emotions in Color",
        'author': 'Clara Dubois',
        'price': 13.00,
        'description': "The Story Behind the Brushstrokes and Bold Hues. Art historian Clara Dubois takes readers inside Van Gogh's tumultuous mind through his use of color.",
        'college': 'Institute of Humanities and Arts',
        'program': 'Art History and Cultural Studies',
        'grade': '3',
        'course': 'Impressionism and Post-Impressionism',
        'category': 'arts',
        'condition': 'like_new',
        'year_published': 2022,
    },
]


class Command(BaseCommand):
    help = 'Add 10 showcase books assigned to Ural Federal University'

    def handle(self, *args, **options):
        sellers = list(User.objects.filter(username__in=['alice', 'bob']))
        if not sellers:
            sellers = list(User.objects.filter(is_superuser=True)[:2])
        if not sellers:
            self.stdout.write(self.style.ERROR('No users found. Run seed_data first.'))
            return

        urfu = University.objects.filter(is_featured=True).first()
        if not urfu:
            urfu = University.objects.filter(name__icontains='Ural Federal').first()
        if not urfu:
            self.stdout.write(self.style.ERROR('UrFU not found. Run seed_data first.'))
            return

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
                university=urfu,
                college=data.get('college', ''),
                program=data.get('program', ''),
                grade=data['grade'],
                course=data['course'],
                condition=data['condition'],
                category=data['category'],
                year_published=data.get('year_published'),
                seller=seller,
            )
            self.stdout.write(f'  Added: {data["title"]}')
            added += 1

        self.stdout.write(self.style.SUCCESS(f'\nDone! Added {added} showcase books.'))
        self.stdout.write('Note: Cover images can be uploaded via Edit on each book listing.')
