"""
books/models.py
Campus Secondhand Book Trading Platform — Core Data Models
校园二手书交易平台 — 核心数据模型
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# ──────────────────────────────────────────────
# University / 大学
# ──────────────────────────────────────────────
class University(models.Model):
    """
    学校模型 / University model.
    管理员可在后台添加/编辑学校，用户也可通过扩展功能请求添加。
    Admins manage universities in the admin panel; users can request additions.
    """
    name = models.CharField(max_length=200, verbose_name='University Name')
    country = models.CharField(max_length=100, default='China', verbose_name='Country')
    abbreviation = models.CharField(max_length=20, blank=True, verbose_name='Abbreviation')
    description = models.TextField(blank=True, verbose_name='Description')
    # 置顶显示（如 UrFU）/ Featured universities appear first in dropdowns
    is_featured = models.BooleanField(default=False, verbose_name='Featured (appears first)')

    class Meta:
        ordering = ['-is_featured', 'name']
        verbose_name = 'University'
        verbose_name_plural = 'Universities'

    def __str__(self):
        return self.name


# ──────────────────────────────────────────────
# College / 学院（按大学归档）
# ──────────────────────────────────────────────
class College(models.Model):
    """
    院系模型 / College or faculty under a university.
    每所大学可维护自己的学院列表，在卖书/筛选表单里下拉选择。
    Each university can maintain its own college list for dropdown selection.
    """
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='colleges')
    name = models.CharField(max_length=200, verbose_name='College Name')
    abbreviation = models.CharField(max_length=30, blank=True, verbose_name='Abbreviation')

    class Meta:
        ordering = ['name']
        unique_together = [('university', 'name')]
        verbose_name = 'College / Faculty'
        verbose_name_plural = 'Colleges / Faculties'

    def __str__(self):
        return f'{self.name} ({self.university.abbreviation or self.university.name})'


# ──────────────────────────────────────────────
# Major / 专业
# ──────────────────────────────────────────────
class Major(models.Model):
    """专业模型 / Academic major or program under a college."""
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='majors')
    name = models.CharField(max_length=200, verbose_name='Major Name')

    class Meta:
        ordering = ['name']
        unique_together = [('college', 'name')]
        verbose_name = 'Major / Program'
        verbose_name_plural = 'Majors / Programs'

    def __str__(self):
        return f'{self.name} ({self.college.name})'


# ──────────────────────────────────────────────
# Book / 书籍
# ──────────────────────────────────────────────
class Book(models.Model):
    """
    二手书模型 / Secondhand book listing model.
    包含学校-学院-专业-年级-课程的完整筛选体系。
    Contains full filtering hierarchy: University > College > Major > Grade > Course.
    """

    CONDITION_CHOICES = [
        ('like_new', 'Like New (98%)'),
        ('good', 'Good (85%)'),
        ('used', 'Used (70%)'),
    ]

    CATEGORY_CHOICES = [
        ('arts', 'Arts & Humanities'),
        ('business', 'Business & Management'),
        ('cs', 'Computer Science & IT'),
        ('math', 'Mathematics & Statistics'),
        ('engineering', 'Engineering'),
        ('education', 'Education'),
        ('social', 'Social Sciences'),
        ('natural', 'Natural Sciences'),
        ('health', 'Health & Medicine'),
        ('other', 'Other'),
    ]

    # Grade choices: Elementary → Middle → High School → Undergrad → Master's → PhD
    GRADE_CHOICES = [
        ('elem', 'Elementary School'),
        ('middle', 'Middle School'),
        ('hs', 'High School'),
        ('1', 'Freshman (Year 1)'),
        ('2', 'Sophomore (Year 2)'),
        ('3', 'Junior (Year 3)'),
        ('4', 'Senior (Year 4)'),
        ('ms1', "Master's Year 1"),
        ('ms2', "Master's Year 2"),
        ('ms3', "Master's Year 3"),
        ('phd1', 'PhD Year 1'),
        ('phd2', 'PhD Year 2'),
        ('phd3', 'PhD Year 3'),
        ('phd4', 'PhD Year 4'),
        ('phd5', 'PhD Year 5+'),
    ]

    # 基本信息 / Basic info
    title = models.CharField(max_length=300, verbose_name='Book Title')
    author = models.CharField(max_length=200, verbose_name='Author')
    price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        verbose_name='Price'
    )
    description = models.TextField(blank=True, verbose_name='Description')
    cover = models.ImageField(
        upload_to='covers/', blank=True, null=True,
        verbose_name='Cover Image'
    )

    # 学校筛选体系 / School hierarchy filters
    university = models.ForeignKey(
        University, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='books', verbose_name='University / 学校'
    )
    # 学院/系 / College or faculty
    college = models.CharField(max_length=200, blank=True, verbose_name='College / Faculty / 学院')
    # 专业 / Major or program
    program = models.CharField(max_length=200, blank=True, verbose_name='Major / Program / 专业')
    # 年级 / Grade level
    grade = models.CharField(
        max_length=10, choices=GRADE_CHOICES, blank=True,
        verbose_name='Grade Level / 年级'
    )
    # 课程 / Course
    course = models.CharField(max_length=200, blank=True, verbose_name='Course / 课程')

    # 图书分类 / Subject category
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, blank=True,
        verbose_name='Category / 分类'
    )
    condition = models.CharField(
        max_length=10, choices=CONDITION_CHOICES, default='good',
        verbose_name='Condition / 成色'
    )
    year_published = models.IntegerField(
        null=True, blank=True, verbose_name='Year Published / 出版年份'
    )

    # 卖家 / Seller
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='books',
        verbose_name='Seller / 卖家'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Listed At / 上架时间')
    is_sold = models.BooleanField(default=False, verbose_name='Is Sold / 已售')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return f'{self.title} by {self.author}'

    @property
    def condition_label(self):
        labels = {
            'like_new': 'Like New (98%)',
            'good': 'Good (85%)',
            'used': 'Used (70%)',
        }
        return labels.get(self.condition, self.condition)

    # 5% 平台服务费计算 / 5% platform service fee
    @property
    def platform_fee_amount(self):
        """平台服务费（5%）/ Platform service fee (5%)"""
        if self.price:
            return round(float(self.price) * 0.05, 2)
        return 0.0

    @property
    def seller_receives(self):
        """卖家实收金额（扣除5%平台费）/ Seller net after 5% platform fee"""
        if self.price:
            return round(float(self.price) * 0.95, 2)
        return 0.0


# ──────────────────────────────────────────────
# Order / 订单
# ──────────────────────────────────────────────
class Order(models.Model):
    """
    订单模型 / Order model.
    平台从每笔交易中收取5%服务费。
    Platform charges a 5% service fee on each transaction.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending / 待确认'),
        ('confirmed', 'Confirmed / 已确认'),
        ('completed', 'Completed / 已完成'),
        ('cancelled', 'Cancelled / 已取消'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='orders')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_bought')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_sold')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True)
    # 5%平台服务费（自动计算）/ 5% platform service fee (auto-calculated)
    platform_fee = models.DecimalField(
        max_digits=8, decimal_places=2, default=0,
        verbose_name='Platform Fee (5%) / 平台服务费'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # 自动计算5%平台服务费 / Auto-calculate 5% platform fee on save
        if self.book_id and self.book.price:
            self.platform_fee = round(float(self.book.price) * 0.05, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Order #{self.pk}: {self.book.title}'


# ──────────────────────────────────────────────
# Message / 聊天消息
# ──────────────────────────────────────────────
class Message(models.Model):
    """站内聊天消息 / In-platform chat message between users"""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    book = models.ForeignKey(
        Book, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender.username} → {self.receiver.username}: {self.text[:40]}'


# ──────────────────────────────────────────────
# Advertisement / 广告位
# ──────────────────────────────────────────────
class Advertisement(models.Model):
    """
    广告位模型 / Advertisement model.
    商业变现手段之一：出租平台广告位，收取广告费。
    Revenue stream: rent advertising slots and charge placement fees.
    """
    title = models.CharField(max_length=200, verbose_name='Ad Title / 广告标题')
    image = models.ImageField(
        upload_to='ads/', blank=True, null=True,
        verbose_name='Ad Image / 广告图片'
    )
    link_url = models.URLField(blank=True, verbose_name='Link URL / 广告链接')
    advertiser_name = models.CharField(
        max_length=200, blank=True, verbose_name='Advertiser / 广告商名称'
    )
    # 广告收费金额（用于后台统计收益）/ Fee charged for this ad placement
    price_paid = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        verbose_name='Price Paid / 广告费用'
    )
    is_active = models.BooleanField(default=True, verbose_name='Active / 是否展示')
    # 排序权重（数字越小越靠前）/ Display order weight (lower = higher priority)
    position = models.IntegerField(default=0, verbose_name='Position / 排序')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(
        null=True, blank=True, verbose_name='Expires At / 到期时间'
    )

    class Meta:
        ordering = ['position', '-created_at']
        verbose_name = 'Advertisement'
        verbose_name_plural = 'Advertisements'

    def __str__(self):
        return f'Ad: {self.title} ({self.advertiser_name})'

    @property
    def is_visible(self):
        """是否可见（未过期且已激活）/ Visible if active and not expired"""
        if not self.is_active:
            return False
        if self.expires_at and timezone.now() > self.expires_at:
            return False
        return True


# ──────────────────────────────────────────────
# Sponsor / 赞助商 & 捐赠人
# ──────────────────────────────────────────────
# ──────────────────────────────────────────────
# BookImage / 书籍附加图片
# ──────────────────────────────────────────────
class BookImage(models.Model):
    """
    书籍额外图片模型 / Extra photos for a book listing.
    允许卖家上传多张照片展示书籍实际状况。
    Allows sellers to upload multiple photos showing the book's real condition.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='book_images/', verbose_name='Photo / 照片')
    caption = models.CharField(max_length=200, blank=True, verbose_name='Caption / 说明')
    order = models.IntegerField(default=0, verbose_name='Order / 排序')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Book Photo'
        verbose_name_plural = 'Book Photos'

    def __str__(self):
        return f'Photo for "{self.book.title}" #{self.pk}'


# ──────────────────────────────────────────────
# Sponsor / 赞助商 & 捐赠人
# ──────────────────────────────────────────────
class Sponsor(models.Model):
    """
    赞助商/捐赠人模型 / Sponsor & donor model.
    商业变现手段之二：接受企业赞助和个人捐赠，展示在网站上增加曝光。
    Revenue stream: accept corporate sponsorships and individual donations.
    """
    TIER_CHOICES = [
        ('platinum', 'Platinum'),
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bronze', 'Bronze'),
        ('donor', 'Individual Donor'),
    ]

    name = models.CharField(max_length=200, verbose_name='Name / 赞助商名称')
    logo = models.ImageField(
        upload_to='sponsors/', blank=True, null=True,
        verbose_name='Logo / 标志图片'
    )
    website = models.URLField(blank=True, verbose_name='Website / 官网链接')
    tier = models.CharField(
        max_length=10, choices=TIER_CHOICES, default='bronze',
        verbose_name='Tier / 赞助等级'
    )
    # 赞助/捐赠金额（用于后台统计）/ Sponsorship or donation amount
    donation_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0,
        verbose_name='Amount / 赞助金额'
    )
    is_active = models.BooleanField(default=True, verbose_name='Active / 是否展示')
    message = models.TextField(blank=True, verbose_name='Message / 赞助商寄语')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['tier', 'name']
        verbose_name = 'Sponsor'
        verbose_name_plural = 'Sponsors'

    def __str__(self):
        return f'{self.get_tier_display()} — {self.name}'
