from django.shortcuts import render

from . import models


def main(request):
    """ The main page for the calculators app. """
    return render(request, 'calculators/main.html')
