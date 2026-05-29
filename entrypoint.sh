#!/bin/sh
# ──────────────────────────────────────────────
# entrypoint.sh — Docker 容器启动脚本 / Container startup script
# ──────────────────────────────────────────────
set -e

echo "=== Campus Secondhand Book Trading Platform ==="
echo "=== 校园二手书交易平台 ==="

# 等待数据库就绪（PostgreSQL 模式时使用；SQLite 直接跳过）
# Wait for DB (relevant when using PostgreSQL; SQLite skips this)
echo "[1/3] Running database migrations / 运行数据库迁移..."
python manage.py migrate --noinput

# 如果没有超级用户，创建默认管理员 / Create default superuser if none exists
echo "[2/3] Checking superuser / 检查超级用户..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@campus.example', 'admin123456')
    print('  Default superuser created: admin / password: admin123456')
    print('  默认管理员已创建: admin / 密码: admin123456')
else:
    print('  Superuser already exists / 已有超级用户')
" 2>/dev/null || true

# 启动 Django 开发服务器 / Start Django development server
# 生产环境请换成 gunicorn / In production, replace with gunicorn
echo "[3/3] Starting server on 0.0.0.0:8000 / 启动服务..."
exec python manage.py runserver 0.0.0.0:8000
