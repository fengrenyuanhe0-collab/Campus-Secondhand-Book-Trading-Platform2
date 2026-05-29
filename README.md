# Campus Secondhand Book Trading Platform
# 校园二手书交易平台

> A full-stack Django web application for trading secondhand textbooks among university students.  
> 面向高校学生的二手教材交易平台，Django 全栈实现。

---

## ✨ Features / 功能特性

### Core / 核心功能
| Feature | 功能 |
|---|---|
| Browse & search books | 浏览与搜索书籍（书名、作者、课程） |
| Filter by university / college / grade / category | 按学校、学院、年级、分类多维筛选 |
| Sort by price or date | 按价格高低或上架时间排序 |
| Book detail with photo gallery | 书籍详情页，支持多图展示 |
| Session-based shopping cart | Session 购物车，支持拖拽加购 |
| Checkout & order management | 结账下单，买卖双方订单历史 |
| In-platform real-time chat | 站内聊天（5秒轮询），买卖方直接沟通 |
| User profiles with academic info | 用户资料，含学校/学院/专业/年级 |

### Commercial / 商业变现
| Stream | 方式 |
|---|---|
| **5% transaction fee** on every sale | 每笔交易收取 **5% 平台服务费** |
| **Paid advertisement slots** | 广告位租售（管理员后台配置） |
| **Sponsorship / Donations** | 赞助商与捐赠展示（铂金/黄金/白银/青铜等级） |

### Technical / 技术亮点
- Django 4.2 + SQLite（可替换为 PostgreSQL）
- Django REST Framework — full REST API (`/api/`)
- Redis cache with local-memory fallback
- Rotating file logs (`logs/app.log`, `logs/error.log`)
- Docker + docker-compose one-command deployment
- Auto-generated gradient book covers (no image needed)
- Drag-to-cart on the home page

---

## 🚀 Quick Start / 快速启动

### Option A — Docker (Recommended) / Docker 部署（推荐）

```bash
# Clone / 克隆
git clone https://github.com/fengrenyuanhe0-collab/Campus-Secondhand-Book-Trading-Platform2.git
cd Campus-Secondhand-Book-Trading-Platform2

# Build & start / 构建并启动
docker compose up -d --build

# Open browser / 打开浏览器
# http://localhost:1234
```

### Option B — Local Python / 本地 Python 运行

```bash
# Install dependencies / 安装依赖
pip install -r requirements.txt

# Migrate / 迁移数据库
python manage.py migrate

# Seed demo data (20 universities + 25 books + 3 users)
# 导入演示数据
python manage.py seed_data

# Run / 启动
python manage.py runserver
# http://127.0.0.1:8000
```

---

## 👤 Demo Accounts / 演示账号

| Username | Password | Role |
|---|---|---|
| `admin` | `admin123456` | Superuser / 超级管理员 |
| `alice` | `password123` | Normal user / 普通用户 |
| `bob` | `password123` | Normal user / 普通用户 |

Admin panel / 管理后台: `http://localhost:1234/admin/`

---

## 📄 Pages / 页面列表

| URL | Description | 说明 |
|---|---|---|
| `/` | Landing page | 落地页 |
| `/home/` | Book marketplace | 书籍市场（搜索+筛选） |
| `/book/<id>/` | Book detail | 书籍详情 |
| `/book/new/` | List a book | 上架新书 |
| `/book/<id>/edit/` | Edit listing | 编辑书籍 |
| `/cart/` | Shopping cart | 购物车 |
| `/checkout/` | Order confirmation | 结账确认 |
| `/orders/` | Order history | 订单历史（买卖双方） |
| `/chat/<user_id>/` | Chat | 站内聊天 |
| `/profile/` | My profile | 个人主页 |
| `/admin/` | Django admin | 管理后台 |

---

## 🔌 REST API

Base URL: `/api/`

| Endpoint | Methods | Description |
|---|---|---|
| `/api/books/` | GET, POST | List / create books |
| `/api/books/<id>/` | GET, PUT, DELETE | Book detail |
| `/api/universities/` | GET | List universities |
| `/api/orders/` | GET, POST | Orders |
| `/api/messages/` | GET, POST | Messages |
| `/api/users/me/` | GET | Current user info |

Filter example / 筛选示例:
```
GET /api/books/?category=cs&grade=2&search=calculus
```

---

## 🗂 Project Structure / 项目结构

```
campus_books_django/
├── campus_books/        Django config (settings, urls, wsgi)
├── books/               Main app
│   ├── models.py        Book, University, Order, Message, Ad, Sponsor
│   ├── views.py         Page views + cart + checkout + chat
│   ├── api_views.py     REST API ViewSets
│   ├── forms.py
│   ├── serializers.py
│   └── management/commands/
│       ├── seed_data.py          20 universities + demo users + 15 books
│       ├── add_showcase_books.py 10 showcase books with real covers
│       └── link_showcase_covers.py  link cover images to DB
├── users/               Auth app — UserProfile model
├── templates/           HTML templates (all pages)
├── static/              CSS, JS, images
├── media/               User-uploaded book covers
├── logs/                app.log + error.log
├── Dockerfile
├── docker-compose.yml
└── entrypoint.sh
```

---

## 🏗 Architecture Notes / 架构说明

### School Hierarchy Filter / 学校层级筛选
```
University → College / Faculty → Major → Grade → Course
大学 → 学院/系 → 专业 → 年级 → 课程
```

### Grade Levels / 年级体系
Elementary → Middle → High School → Undergraduate (Y1–Y4) → Master's (Y1–Y3) → PhD (Y1–Y5+)

### Monetization / 商业逻辑
- Each `Book` exposes `platform_fee_amount` (5%) and `seller_receives` (95%) properties
- Each `Order` auto-calculates and stores `platform_fee` on save
- `Advertisement` model tracks `price_paid` per ad placement
- `Sponsor` model tracks `donation_amount` per sponsor tier

---

## 🐳 Docker Details / Docker 说明

```yaml
# docker-compose.yml highlights
ports:   "1234:8000"       # host:container
volumes:
  - ./media:/app/media     # persistent uploads
  - ./db.sqlite3:/app/db.sqlite3
  - ./logs:/app/logs
restart: unless-stopped
```

The `entrypoint.sh` runs on every start:
1. `python manage.py migrate` — apply pending migrations
2. Create default superuser if none exists
3. `python manage.py runserver 0.0.0.0:8000`

---

## 📦 Requirements / 主要依赖

```
Django==4.2.30
djangorestframework==3.16.0
Pillow==11.2.1
django-redis==5.4.0
```

---

## 📝 License / 许可

This project is for educational purposes.  
本项目为课程作业，仅供学习参考。

---

*Built with Django 4.2 · Deployed via Docker · Ural Federal University*  
*基于 Django 4.2 构建 · Docker 一键部署 · 乌拉尔联邦大学*
