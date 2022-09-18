from dataclasses import field
from django.forms import ModelForm
from .models import HackerNews

class HackerNewsForm(ModelForm):
    class Meta:
        model = HackerNews
        fields = ['hackernewsid','host','by', 'category', 'title', 'text', 'urls',]