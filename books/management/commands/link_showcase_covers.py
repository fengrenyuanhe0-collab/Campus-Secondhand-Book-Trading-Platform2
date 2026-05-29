"""
Run: python manage.py link_showcase_covers
Copies the 10 showcase cover images from static/img/covers/ to media/covers/
and updates each Book record accordingly.
"""
import shutil
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from books.models import Book

# Ordered titles matching images (1).png → (10).png
TITLE_TO_IMG = [
    ('Cosmic Wonders: A Journey Through Space',                   '校园二手书交易平台开发 (1).png',  'showcase_cosmic_wonders.png'),
    ('The Silk Road: Echoes of Ancient Trade',                    '校园二手书交易平台开发 (2).png',  'showcase_silk_road.png'),
    ("The Mind's Mirror: Understanding Self-Perception",          '校园二手书交易平台开发 (3).png',  'showcase_minds_mirror.png'),
    ('Questions Without Answers: Existentialism in Modern Life',  '校园二手书交易平台开发 (4).png',  'showcase_questions.png'),
    ('Our Changing Planet: Climate, Landscapes, and Human Impact','校园二手书交易平台开发 (5).png',  'showcase_changing_planet.png'),
    ('Harmony of the Spheres: Music and the Universe',            '校园二手书交易平台开发 (6).png',  'showcase_harmony.png'),
    ('Whispers in the Attic',                                     '校园二手书交易平台开发 (7).png',  'showcase_whispers.png'),
    ('The Beauty of Numbers: Patterns in Nature and Art',         '校园二手书交易平台开发 (8).png',  'showcase_beauty_numbers.png'),
    ("Life's Blueprint: DNA and the Code of Evolution",           '校园二手书交易平台开发 (9).png',  'showcase_lifes_blueprint.png'),
    ("Van Gogh's Palette: Emotions in Color",                     '校园二手书交易平台开发 (10).png', 'showcase_van_gogh.png'),
]


class Command(BaseCommand):
    help = 'Link showcase book cover images to database records'

    def handle(self, *args, **options):
        src_dir = Path(settings.BASE_DIR) / 'static' / 'img' / 'covers'
        dst_dir = Path(settings.MEDIA_ROOT) / 'covers'
        dst_dir.mkdir(parents=True, exist_ok=True)

        updated = 0
        for title, src_name, dst_name in TITLE_TO_IMG:
            src = src_dir / src_name
            dst = dst_dir / dst_name

            if not src.exists():
                self.stdout.write(self.style.WARNING(f'  Source not found: {src_name}'))
                continue

            # Copy to media/covers/
            shutil.copy2(src, dst)

            # Update database — find book by title
            qs = Book.objects.filter(title=title)
            if not qs.exists():
                self.stdout.write(self.style.WARNING(f'  Book not found in DB: {title}'))
                continue

            qs.update(cover=f'covers/{dst_name}')
            self.stdout.write(f'  Linked: {title[:45]:<45} ← {dst_name}')
            updated += 1

        self.stdout.write(self.style.SUCCESS(f'\nDone! Updated {updated} book covers.'))
