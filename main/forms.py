from django import forms
from .models import Tag, Comment
from django.core.exceptions import ValidationError


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title', 'slug']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control m-0'}),
            'slug': forms.TextInput(attrs={'class': 'form-control m-0'}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise ValidationError('Slug may not "create"')
        if Tag.objects.filter(slug__iexact=new_slug):
            raise ValidationError('Slug "{}" already exist'.format(new_slug))
        return new_slug


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['nickname', 'text', 'post']

        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя...'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Комментарий...'}),
            'post': forms.NumberInput()
        }

    def clean_nickname(self):
        new_nickname = self.cleaned_data['nickname']
        if new_nickname == 'debil':
            raise ValidationError('Sam ti debil')
        return new_nickname
