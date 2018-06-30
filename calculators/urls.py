from django.urls import path

from . import views


app_name = 'calculators'
urlpatterns = [
    path('', views.main, name='main'),
]
