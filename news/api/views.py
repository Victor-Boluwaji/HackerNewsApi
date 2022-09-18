from calendar import c
from django.http import HttpResponse
from random import randint
from unicodedata import category
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from unittest import result
from urllib import response
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.core.paginator import Paginator
import json
import requests
from .models import HackerNews
from .forms import HackerNewsForm

def loginpage(request):
    page='login'

    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'Username and password does not match')
    
    context = {'page':page}
    return render (request, 'api/reg_login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('homepage')


def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'An error occured during registeration ')


    context = {'form': form }
    return render (request, 'api/reg_login.html', context)




def homepage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    #This is to query the db
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
    dat = HackerNews.objects.all()
    data = dat.get(hackernewsid=pk)
    response = data.kids
    if response is None:
        comments={}
    else:
        result = response.split(',')[1:len(response.split(','))-2] # in order to trim the last element
        last = response.split(',')[-1] # got this from API " 499287535 ] /n" --> reshaped to that below
        result.insert(len(result), last.strip().split()[0]) # "499287535"
        res = [int(id.strip('[]')) for id in result]
        comments = []
        for id in res:
            NEWS_URL = f'https://hacker-news.firebaseio.com/v0/item/{str(id)}.json?print=pretty'
            response = requests.get(NEWS_URL)
            comment = json.loads(response.text)
            comments.append(comment)

    context = {
        'data':data, 'comments':comments
    }
    return render (request, 'api/detail.html', context)


@login_required(login_url='login')
def create_news(request):
    form = HackerNewsForm()
    if request.method =='POST':

        
        form = HackerNewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('homepage')
    context = {'form':form}
    return render (request, 'api/news_create.html', context)

@login_required(login_url='login')
def update_news(request, pk):
    news = HackerNews.objects.get(hackernewsid=pk)
    form = HackerNewsForm(instance=news)

    if request.user != news.host:
        return HttpResponse('You do Not have the permission')

    if request.method == 'POST':
        form = HackerNewsForm(request.POST, instance=news)

        if form.is_valid():
            form.save()
            return redirect ('homepage')
    context = {'form': form}
    return render (request, 'api/news_create.html', context)


@login_required(login_url='login')
def delete_news(request, pk):
    news = HackerNews.objects.get(hackernewsid=pk)
    if request.user != news.host:
        return HttpResponse('You do Not have the permission')

    if request.method == 'POST':
        news.delete()
        return redirect('homepage')
    context = {'news':news}
    return render (request, 'api/delete.html', context)