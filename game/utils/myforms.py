from django import forms
from game.models import *
from django_ckeditor_5.widgets import CKEditor5Widget


class SiteModelForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['site_url', 'site_name', 'logo', 'title', 'description', 'aboutus', 'copyright', 'contactus',
                  'Privacypolicy', 'Termofuse']
        widgets = {
            'site_url': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 550px;'}),  # 增加宽度
            'site_name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 550px;'}),  # 增加宽度
            'title': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 550px;'}),  # 增加宽度
            'description': forms.Textarea(attrs={'class': 'form-control', 'style': 'width: 550px;'}),  # 增加宽度
            'aboutus': CKEditor5Widget(),
            'copyright': CKEditor5Widget(),
            'contactus': CKEditor5Widget(),
            'Privacypolicy': CKEditor5Widget(),
            'Termofuse': CKEditor5Widget(),
        }


class GameModelForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'slug', 'description', 'thumbnail', 'description', 'iframeUrl', 'recommend', 'site','is_checked',
                  'whatis', 'HowtoPlay']
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'margin: 20px;width: 500px; display: inline-block;'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'style': 'margin: 20px;width: 500px; display: inline-block;'}),
            'description': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'margin: 20px;width: 500px; display: inline-block;'}),
            'thumbnail': forms.ClearableFileInput(attrs={'style': 'display:none;'}),  # 隐藏thumbnail输入框
            'iframeUrl': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'margin: 25px;width: 500px; display: inline-block;'}),
            'recommend': forms.Select(attrs={'class': 'form-control', 'style': 'margin: 20px;width: 250px; display: inline-block;'}),
            'site': forms.Select(attrs={'class': 'form-control', 'style': 'margin: 20px;width: 250px; display: inline-block;'}),
            'whatis': forms.Textarea(attrs={'class': 'form-control','style': 'margin: 20px;width: 600px; display: inline-block;'}),
            'HowtoPlay': forms.Textarea(attrs={'class': 'form-control','style': 'margin: 20px;width: 600px; display: inline-block;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].widget.attrs.update({
            'disabled': 'disabled',  # 禁用
        })


class QuestionsModelForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['question', 'answer']
        widgets = {
            'question': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width: 400px; display: inline-block;'}),
            'answer': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 400px; display: inline-block;'}),
        }
