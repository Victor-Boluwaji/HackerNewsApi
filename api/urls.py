from django.urls import path
#from .views import NewsIdView, NewsItemView
from . import views

urlpatterns = [
    path ('',views.homepage, name='homepage'),
    path ('trial/<str:pk>/',views.details, name='details')
 
]