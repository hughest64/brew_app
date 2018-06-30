# views for the recipes app
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .helpers import uploader

from . import forms, models


def recipe_list(request):
    """ The main recipes page. Returns a view with a list of all recipes. """
    recipes = models.Recipe.objects.all()
    form = forms.UploadXMLFileForm()
    if request.method == 'POST':
         uploader.upload_file(request)
    context = {'recipes': recipes, 'form': form}
    return render(request, 'recipes/recipe_list.html', context)


def recipe_detail(request, pk, slug):
    """ Returns the view with the details of a given recipe. """
    try:
        recipe = models.Recipe.objects.prefetch_related(
            'mashstep_set', 'hop_set', 'miscellaneous_set', 'yeast_set'
        ).get(pk=pk)

    except models.Recipe.DoesNotExist:
        raise Http404

    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})


def recipe_sessions(request, recipe_pk):
    """ A list of all sessions for a given recipe. """
    recipe = get_object_or_404(models.Recipe, id=recipe_pk)
    sessions = recipe.session_set.order_by('created_at')
    context = {'recipe': recipe, 'sessions': sessions}
    return render(request, 'recipes/session_list.html', context)


def new_session(request, recipe_pk):
    """ The start of a new brew session. Redirects to session_timer. """
    recipe = models.Recipe.objects.get(id=recipe_pk)
    return render(request, 'recipes/new_session.html', {'recipe': recipe})


def session_context(recipe_pk, session_pk):
    """ Helper function that returns the context dict for session views."""
    session = get_object_or_404(
        models.Session, recipe_id=recipe_pk, id=session_pk
    )
    recipe = models.Recipe.objects.get(id=recipe_pk)
    context = {'session': session, 'recipe': recipe}
    return context


def session_detail(request, recipe_pk, session_pk):
    """ Details of a given brew session. """
    context = session_context( recipe_pk, session_pk)
    return render(request, 'recipes/session_detail.html', context)


def session_timer(request, recipe_pk, session_pk):
    """ The timer for an individual brew session. """
    context = session_context(recipe_pk, session_pk )
    return render(request, 'recipes/session_timer.html', context)
