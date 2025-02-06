from django import forms
from game.models import *


class SiteModelForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['site_url', 'site_name', 'logo', 'title', 'description', 'aboutus', 'copyright', 'contactus',
                  'Privacypolicy', 'Termofuse']
        widgets = {
            'site_url': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 550px;'}),  # 增加宽度
            'site_name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 550px;'}),  # 增加宽度
            'title': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 550px;'}),  # 增加宽度
            'description': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 550px;'}),  # 增加宽度
            'aboutus': forms.Textarea(attrs={'class': 'form-control'}),
            'copyright': forms.Textarea(attrs={'class': 'form-control'}),
            'contactus': forms.Textarea(attrs={'class': 'form-control'}),
            'Privacypolicy': forms.Textarea(attrs={'class': 'form-control'}),
            'Termofuse': forms.Textarea(attrs={'class': 'form-control'}),
        }


class GameModelForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'slug', 'description', 'thumbnail', 'description', 'iframeUrl', 'recommend', 'is_checked',
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
            'recommend': forms.Select(attrs={'class': 'form-control', 'style': 'margin: 20px;width: 500px; display: inline-block;'}),
            # 'content': forms.Textarea(attrs={'class': 'form-control'}),
            'whatis': forms.Textarea(attrs={'class': 'form-control'}),
            'HowtoPlay': forms.Textarea(attrs={'class': 'form-control'}),
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
