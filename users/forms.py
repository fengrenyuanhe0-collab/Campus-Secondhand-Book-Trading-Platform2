"""
users/forms.py
Registration and profile forms / 注册表单与用户资料表单
"""
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from books.models import University


class RegisterForm(forms.Form):
    """用户注册表单 / User registration form"""
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Username / 用户名'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'input', 'placeholder': 'your@email.com'}),
    )
    password = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': '••••••••'}),
    )
    password2 = forms.CharField(
        label='Confirm Password / 确认密码',
        widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': '••••••••'}),
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken. / 用户名已被使用')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists. / 该邮箱已注册')
        return email

    def clean(self):
        data = super().clean()
        if data.get('password') != data.get('password2'):
            raise forms.ValidationError('Passwords do not match. / 两次密码不一致')
        return data


class ProfileForm(forms.ModelForm):
    """用户资料编辑表单 / User profile edit form"""

    class Meta:
        model = UserProfile
        fields = ['university', 'college', 'major', 'grade', 'phone', 'bio']
        widgets = {
            'university': forms.Select(attrs={'class': 'input'}),
            'college': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'e.g. College of Computer Science / 计算机学院',
            }),
            'major': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'e.g. Software Engineering / 软件工程',
            }),
            'grade': forms.Select(attrs={'class': 'input'}),
            'phone': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Contact number (optional) / 联系电话（可选）',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'input', 'rows': 3,
                'placeholder': 'A short bio... / 自我介绍',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['university'].queryset = University.objects.all()
        self.fields['university'].empty_label = 'Select University'
        self.fields['grade'].empty_label = 'Select Grade'
        # 所有字段均可选 / All fields are optional
        for field in self.fields.values():
            field.required = False
