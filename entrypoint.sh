#!/bin/sh
# entrypoint.sh — Docker container startup script
set -e

echo "=== Campus Secondhand Book Trading Platform ==="
echo "=== 校园二手书交易平台 ==="

# ── Wait for PostgreSQL / 等待 PostgreSQL 就绪 ──
echo "[0/4] Waiting for PostgreSQL at ${POSTGRES_HOST:-db}:${POSTGRES_PORT:-5432}..."
until python -c "
import os, sys, psycopg2
try:
    psycopg2.connect(
        dbname=os.environ.get('POSTGRES_DB','campus_books'),
        user=os.environ.get('POSTGRES_USER','campus'),
        password=os.environ.get('POSTGRES_PASSWORD','campus_pass'),
        host=os.environ.get('POSTGRES_HOST','db'),
        port=os.environ.get('POSTGRES_PORT','5432'),
    )
    sys.exit(0)
except Exception:
    sys.exit(1)
" 2>/dev/null; do
  echo "  PostgreSQL not ready, retrying in 2s..."
  sleep 2
done
echo "  PostgreSQL is ready."

# ── Migrate / 迁移数据库 ──
echo "[1/4] Running database migrations / 运行数据库迁移..."
python manage.py migrate --noinput

# ── Seed demo data if DB is empty / 首次启动导入演示数据 ──
echo "[2/4] Seeding demo data if needed / 首次启动导入演示数据..."
python manage.py shell -c "
from books.models import Book
if Book.objects.count() == 0:
    import subprocess, sys
    subprocess.run([sys.executable, 'manage.py', 'seed_data'], check=True)
    subprocess.run([sys.executable, 'manage.py', 'add_showcase_books'], check=True)
    subprocess.run([sys.executable, 'manage.py', 'link_showcase_covers'], check=True)
    print('  Demo data seeded.')
else:
    print('  Data already exists, skipping seed.')
" 2>/dev/null || true

# ── Superuser / 超级用户 ──
echo "[3/4] Checking superuser / 检查超级用户..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin','admin@campus.example','admin123456')
    print('  Superuser created: admin / admin123456')
else:
    print('  Superuser already exists.')
" 2>/dev/null || true

# ── Collect static files / 收集静态文件 ──
echo "[4/4] Collecting static files / 收集静态文件..."
python manage.py collectstatic --noinput --clear -v 0

# ── Start Gunicorn / 启动 Gunicorn ──
echo "Starting Gunicorn on 0.0.0.0:8000..."
exec gunicorn campus_books.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
