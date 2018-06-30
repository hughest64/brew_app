from django.shortcuts import render

from . import models


def main(request):
    """ The main page for the Timer app. """
    return render(request, 'timer/main.html')
