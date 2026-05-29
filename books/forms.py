"""
books/forms.py — Book listing form
"""
from django import forms
from .models import Book, University


class BookForm(forms.ModelForm):
    """Form for creating or editing a secondhand book listing."""

    class Meta:
        model = Book
        fields = [
            'title', 'author', 'price', 'description', 'cover',
            'university', 'college', 'program', 'grade', 'course',
            'category', 'condition', 'year_published',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Book title'}),
            'author': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Author name'}),
            'price': forms.NumberInput(attrs={
                'class': 'input', 'placeholder': 'Leave blank for free / donation',
                'step': '0.01', 'min': '0',
            }),
            'description': forms.Textarea(attrs={
                'class': 'input', 'rows': 4,
                'placeholder': 'Describe condition, edition, any notes…',
            }),
            'university': forms.Select(attrs={'class': 'input', 'id': 'id_university'}),
            # College uses datalist for autocomplete + free text / 学院支持自动补全也可手动输入
            'college': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'e.g. Institute of Physics and Technology',
                'list': 'college-suggestions',
                'id': 'id_college',
                'autocomplete': 'off',
            }),
            'category': forms.Select(attrs={'class': 'input'}),
            'program': forms.TextInput(attrs={
                'class': 'input', 'placeholder': 'e.g. Computer Science',
            }),
            'grade': forms.Select(attrs={'class': 'input'}),
            'course': forms.TextInput(attrs={
                'class': 'input', 'placeholder': 'e.g. Data Structures',
            }),
            'condition': forms.Select(attrs={'class': 'input'}),
            'year_published': forms.NumberInput(attrs={
                'class': 'input', 'placeholder': 'e.g. 2022',
                'min': '1900', 'max': '2030',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Iterate items() to get both field name and field object
        # field objects don't have a .name attribute — the name is the dict key
        for name, field in self.fields.items():
            field.required = name in ('title', 'author')
        self.fields['price'].required = False
        self.fields['university'].queryset = University.objects.all()
        self.fields['university'].empty_label = 'Select University'
        self.fields['category'].empty_label = 'Select Category'
        self.fields['grade'].empty_label = 'Select Grade Level'
