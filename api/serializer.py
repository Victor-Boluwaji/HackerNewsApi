from rest_framework import serializers
from .models import HackerNews

class NewsIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = HackerNews
        fields = '__all__'