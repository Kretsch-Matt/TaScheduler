from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('create-account/', views.createAccount, name='createAccount'),


]