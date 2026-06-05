"""
books/admin.py
Django 后台管理注册 / Django admin registration
商业模型（广告、赞助商）可在后台直接管理。
Commercial models (ads, sponsors) are manageable in the admin panel.
"""
from django.contrib import admin
from .models import University, Book, Order, Message, Advertisement, Sponsor, BookImage, College, Major


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'university', 'college', 'category', 'grade', 'condition', 'seller', 'is_sold', 'created_at')
    list_filter = ('category', 'grade', 'condition', 'is_sold', 'university')
    search_fields = ('title', 'author', 'course', 'program', 'college')
    list_editable = ('is_sold',)
    raw_id_fields = ('seller', 'university')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Basic Info / 基本信息', {'fields': ('title', 'author', 'price', 'cover', 'description')}),
        # 完整学校筛选体系 / Full school hierarchy
        ('Academic / 学术信息', {'fields': ('university', 'college', 'program', 'grade', 'course', 'category')}),
        ('Details / 详情', {'fields': ('condition', 'year_published', 'is_sold')}),
        ('Meta', {'fields': ('seller', 'created_at')}),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'book', 'buyer', 'seller', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('book__title', 'buyer__username', 'seller__username')
    raw_id_fields = ('book', 'buyer', 'seller')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'book', 'text', 'created_at', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('sender__username', 'receiver__username', 'text')
    raw_id_fields = ('sender', 'receiver', 'book')


@admin.register(University)
class UniversityAdminNew(admin.ModelAdmin):
    list_display = ('name', 'country', 'abbreviation', 'is_featured')
    search_fields = ('name', 'country')
    list_filter = ('country', 'is_featured')
    list_editable = ('is_featured',)


# 学院管理 / College admin
@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation', 'university')
    search_fields = ('name', 'university__name')
    list_filter = ('university',)
    raw_id_fields = ('university',)


# 专业管理 / Major admin
@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ('name', 'college', 'college__university')
    search_fields = ('name', 'college__name', 'college__university__name')
    list_filter = ('college__university',)
    raw_id_fields = ('college',)

    def college__university(self, obj):
        return obj.college.university
    college__university.short_description = 'University'


# 书籍额外图片管理 / BookImage admin
@admin.register(BookImage)
class BookImageAdmin(admin.ModelAdmin):
    list_display = ('book', 'order', 'uploaded_at')
    raw_id_fields = ('book',)


# 广告位管理 / Advertisement admin — manage ad placements and revenue
@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'advertiser_name', 'price_paid', 'is_active', 'position', 'expires_at', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'advertiser_name')
    list_editable = ('is_active', 'position')
    fieldsets = (
        ('Ad Content / 广告内容', {'fields': ('title', 'image', 'link_url', 'advertiser_name')}),
        ('Commercial / 商业信息', {'fields': ('price_paid', 'is_active', 'position', 'expires_at')}),
    )


# 赞助商/捐赠人管理 / Sponsor & donor admin — manage sponsorships and donations
@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name', 'tier', 'donation_amount', 'is_active', 'created_at')
    list_filter = ('tier', 'is_active')
    search_fields = ('name',)
    list_editable = ('is_active',)
    fieldsets = (
        ('Sponsor Info / 赞助商信息', {'fields': ('name', 'logo', 'website', 'message')}),
        ('Commercial / 商业信息', {'fields': ('tier', 'donation_amount', 'is_active')}),
    )
