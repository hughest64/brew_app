
"""brew_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

# load staticfiles during dev, remove in production
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    # the recipe app
    path('recipes/', include('recipes.urls', namespace='recipes')),
    # the timer app
    path('timer/', include('timer.urls', namespace='timer')),
    # the calculators app
    path('calculators/', include('calculators.urls', namespace='calculators')),

    path('admin/', admin.site.urls),
    # the home page
    path('', views.index, name='index'),
    # account pages
    path('accounts/', include('django.contrib.auth.urls')),
]

# load staticfiles during dev, remove in production
urlpatterns += staticfiles_urlpatterns()
