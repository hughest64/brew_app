from django.urls import path

from . import views


app_name = 'timer'
urlpatterns = [
    path('', views.main, name='main')
]
