# ──────────────────────────────────────────────
# Dockerfile — Campus Secondhand Book Trading Platform
# 校园二手书交易平台 Docker 镜像构建文件
# ──────────────────────────────────────────────

# 使用官方 Python 3.11 slim 镜像 / Use official Python 3.11 slim image
FROM python:3.11-slim

# 设置工作目录 / Set working directory
WORKDIR /app

# 设置 Python 环境变量 / Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=campus_books.settings

# 安装系统依赖（Pillow 需要 libjpeg）/ Install system deps (Pillow needs libjpeg)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制并安装 Python 依赖 / Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码 / Copy project source code
COPY . .

# 创建必要目录 / Create necessary directories
RUN mkdir -p media staticfiles logs

# Static files are collected at runtime in entrypoint.sh
# (needs DB connection which isn't available at build time)

# 复制并设置入口脚本 / Copy and set entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 开放端口 / Expose port
EXPOSE 8000

# 入口点 / Entrypoint
ENTRYPOINT ["/entrypoint.sh"]
