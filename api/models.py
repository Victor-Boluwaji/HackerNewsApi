from django.db import models
from datetime import datetime

# Create your models here.
class HackerNews(models.Model):
    hackernewsid = models.BigIntegerField(unique=True, primary_key=True,)
    by = models.CharField(max_length=300, null=True)
    category = models.CharField(max_length=250, null=True)
    title = models.TextField(null=True)
    text = models.TextField(blank=True, null=True)
    urls = models.URLField(max_length=300, blank=True, null=True)
    kids = models.TextField(blank=True, null=True)
    fetched_at = models.DateTimeField(default=datetime.now())
    #created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField (auto_now=True)


    class Meta:
        ordering = ['-updated']


    
    def __str__(self):
        return str(self.hackernewsid)
