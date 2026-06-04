"""
users/forms.py
Registration and profile forms / 注册表单与用户资料表单
"""
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from books.models import University, College, Major


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
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean(self):
        data = super().clean()
        if data.get('password') != data.get('password2'):
            raise forms.ValidationError('Passwords do not match.')
        return data


class ProfileForm(forms.ModelForm):
    """用户资料编辑表单 / User profile edit form"""

    class Meta:
        model = UserProfile
        fields = ['university', 'college', 'major', 'grade', 'phone', 'bio']
        widgets = {
            'university': forms.Select(attrs={'class': 'input', 'id': 'id_university'}),
            'college':    forms.Select(attrs={'class': 'input', 'id': 'id_college'}),
            'major':      forms.Select(attrs={'class': 'input', 'id': 'id_major'}),
            'grade':      forms.Select(attrs={'class': 'input'}),
            'phone': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Contact number (optional)',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'input', 'rows': 3,
                'placeholder': 'A short bio...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['university'].queryset = University.objects.all()
        self.fields['university'].empty_label = '— Select University —'
        self.fields['grade'].empty_label = '— Select Year / Grade —'

        # Populate college dropdown based on current university
        instance = kwargs.get('instance')
        if instance and instance.university_id:
            self.fields['college'].queryset = College.objects.filter(
                university=instance.university
            )
            self.fields['college'].empty_label = '— Select College / Faculty —'
        else:
            self.fields['college'].queryset = College.objects.none()
            self.fields['college'].empty_label = '— Select University first —'

        # Populate major dropdown based on current college
        if instance and instance.college_id:
            self.fields['major'].queryset = Major.objects.filter(
                college=instance.college
            )
            self.fields['major'].empty_label = '— Select Major —'
        else:
            self.fields['major'].queryset = Major.objects.none()
            self.fields['major'].empty_label = '— Select College first —'

        for field in self.fields.values():
            field.required = False
