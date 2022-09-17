from unicodedata import category
from django.shortcuts import render
from unittest import result
from urllib import response
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
import json
import requests
from .models import HackerNews


def homepage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    result = HackerNews.objects.filter(
        Q(category__icontains=q) |
        Q(title__icontains=q) | 
        Q(by__icontains=q)
    )
    pageinator = Paginator(result, 25)

    page_num = request.GET.get('page')


    page = pageinator.get_page(page_num)

    result_count = result.count()

    context = {'result': result, 'result_count':result_count, 'page':page}
    return render (request, 'api/home.html', context)

def details(request, pk):
    data = HackerNews.objects.get(hackernewsid=pk)
    context = {
        'data':data
    }
    return render (request, 'api/detail.html', context)

