"""
users/models.py
Campus Secondhand Book Trading Platform — User Profile Model
校园二手书交易平台 — 用户资料模型
"""
from django.db import models
from django.contrib.auth.models import User
from books.models import University, College, Major


# ──────────────────────────────────────────────
# UserProfile / 用户资料
# ──────────────────────────────────────────────
class UserProfile(models.Model):
    """
    用户资料模型 / User profile model.
    记录学校-学院-专业-年级信息，用于精准匹配所需书籍。
    Stores school hierarchy info to help users find books for their courses.
    """

    # 与 Book 模型相同的扩展年级选项 / Same expanded grade choices as Book model
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

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # 学校 / University
    university = models.ForeignKey(
        University, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='University / 学校'
    )
    # 学院/系 / College or faculty
    college = models.ForeignKey(
        College, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='College / Faculty / 学院'
    )
    # 专业 / Major
    major = models.ForeignKey(
        Major, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Major / 专业'
    )
    # 年级 / Grade
    grade = models.CharField(
        max_length=10, choices=GRADE_CHOICES, blank=True,
        verbose_name='Grade / 年级'
    )
    bio = models.TextField(blank=True, verbose_name='Bio / 自我介绍')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Phone / 电话')

    class Meta:
        verbose_name = 'User Profile / 用户资料'
        verbose_name_plural = 'User Profiles / 用户资料列表'

    def __str__(self):
        return f'{self.user.username} profile'

    @property
    def display_name(self):
        """优先显示真实姓名，否则显示用户名 / Prefer full name over username"""
        full = self.user.get_full_name()
        return full if full else self.user.username

    @property
    def grade_label(self):
        """获取年级的可读标签 / Human-readable grade label"""
        return dict(self.GRADE_CHOICES).get(self.grade, '')
