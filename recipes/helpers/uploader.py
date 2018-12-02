from django.contrib import messages
from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponseRedirect
from django.urls import reverse

from recipes import models, forms

from .xml_parser import BeerXMLParser


def upload_file(request):
    """ Processes the form data for adding a new recipe to the database. """
    form = forms.UploadXMLFileForm(request.POST, request.FILES)
    if form.is_valid():
        file = request.FILES['file']
        try:
            recipe_file = BeerXMLParser(file)
            recipe_file.parse_file()

        except (SyntaxError, AttributeError):
            messages.error(request,
                "The file must be in Beer XML format." + " "
                + "Please choose a different file."
            )
        else:
            recipe_data = recipe_file.get_all_data() 
            create_recipe(request, recipe_data)
            return HttpResponseRedirect(reverse('recipes:recipe_list'))


def create_recipe(request, data):
    """ Creates a Recipe instance and assigns all the attributes. """
    basic_data = data['basic_data']
    try:
        recipe, created = models.Recipe.objects.get_or_create(
            recipe_name=basic_data['recipe_name'],
            version=basic_data['version'],
            defaults=basic_data
        )
    except MultipleObjectsReturned:
        messages.error(request,
                'Multiple versions of this recipe already exists!'
            )

    else:
        if created:
            create_instance_set(models.MashStep, recipe, data['mash_steps'])
            create_instance_set(models.Hop, recipe, data['hops'])
            create_instance_set(
                models.Fermentable, recipe, data['fermentables']
            )
            create_instance_set(models.Miscellaneous, recipe, data['misc'])
            create_instance_set(models.Yeast, recipe, data['yeast'])
            messages.success(request,
                'The recipe was successfully added. Now get brewing!'
            )
        else:
            messages.error(
                request, 'This recipe version already exists!'
            )


def create_instance_set(model, recipe, data):
    """ Creates and saves recipe related objects (I.E. ingredients, etc) to
    the database.
    """
    model.objects.bulk_create([
        model(**value, recipe=recipe, order=order)
        for order, value in enumerate(data, start=1)
    ])
