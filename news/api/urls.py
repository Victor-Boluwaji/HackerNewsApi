from django.urls import path
#from .views import NewsIdView, NewsItemView
from . import views

urlpatterns = [
    path ('login/', views.loginpage, name='login'),
    path ('logout/', views.logoutUser, name='logout'),
    path ('register/', views.registerPage, name='register'),
    path ('',views.homepage, name='homepage'),
    path ('trial/<str:pk>/',views.details, name='details'),
    path ('create_room/', views.create_news, name='create_news'),
    path ('update_room/<str:pk>/', views.update_news, name='update_news'),
    path ('delete_room/<str:pk>/', views.delete_news, name='delete_news'),
 
]