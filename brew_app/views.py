from django.shortcuts import render

def index(request):
    """ The home page for the main site. """
    return render(request, 'index.html')
