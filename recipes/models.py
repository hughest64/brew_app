from django.db import models

from django.urls import reverse


class Recipe(models.Model):
    """ A beer recipe. All fields except created_at are
    from a Beer XML file.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    recipe_name = models.CharField(max_length=100)
    version = models.FloatField(default=0)
    style = models.CharField(max_length=100, default='')
    boil_time = models.IntegerField()
    brew_type = models.CharField(max_length=100)
    batch_volume = models.DecimalField(max_digits=5, decimal_places=2)
    og = models.DecimalField(max_digits=4, decimal_places=3)
    abv = models.DecimalField(max_digits=4, decimal_places=2)
    boil_volume = models.DecimalField(
        max_digits=5, decimal_places=2
    )
    efficiency = models.DecimalField(max_digits=4, decimal_places=2)
    strike_volume = models.DecimalField(max_digits=4, decimal_places=1)
    strike_temp = models.DecimalField(max_digits=4, decimal_places=1)
    boil_grav = models.DecimalField(max_digits=5, decimal_places=3)

    def __str__(self):
        return "{} - Ver {}".format(self.recipe_name, self.version)

    def get_absolute_url(self):
        """ The URL to the details of a particular recipe. The slug is
        a readable URL string to identify the recipe name and version.
        """
        slug_name = '{} v{}'.format(
            self.recipe_name, self.version
        ).lower().replace(' ', '-')

        return reverse(
            'recipes:recipe_detail',
            kwargs={'slug': slug_name, 'pk': self.id}
        )


class MashStep(models.Model):
    """ The mash steps for a given recipe. """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    temp = models.DecimalField(max_digits=4, decimal_places=1)
    time = models.IntegerField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order',]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """ An abstract class for common ingredient attributes. """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type_of = models.CharField('type', max_length=100)
    amount = models.FloatField()
    order = models.IntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ['order',]


class Hop(Ingredient):
    """ The hops for a given recipe. """
    time = models.IntegerField()
    use = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Fermentable(Ingredient):
    """ The fermentable ingredients in a recipe. """

    def __str__(self):
        return self.name


class Miscellaneous(Ingredient):
    """ Miscellaneous ingredients for a recipe. """
    time = models.CharField(max_length=100)
    use = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'miscellaneous'

    def __str__(self):
        return self.name


class Yeast(Ingredient):
    """ yeasts for a recipe. """
    lab = models.CharField(max_length=100)
    product_id = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'yeast'

    def __str__(self):
        return self.name

# add a model form for this moddel to forms.py
class Session(models.Model):
    """ An individual brew session for a given recipe. """
    created_at = models.DateTimeField(auto_now_add=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    memo = models.TextField()

    NOT_STARTED = 'NS'
    BREWING = 'BB'
    FERMENTING = 'BF'
    COMPLETED = 'BC'
    STATUS_CHOICES = (
        (NOT_STARTED, 'not started'),
        (BREWING, 'brewing'),
        (FERMENTING, 'fermenting'),
        (COMPLETED, 'completed')
    )
    status = models.CharField(
        max_length = 2,
        choices = STATUS_CHOICES,
        default = NOT_STARTED,
    )

    pre_boil_grav = models.DecimalField(
        max_digits=5, decimal_places=3, default=0.000
    )
    post_boil_grav = models.DecimalField(
        max_digits=5, decimal_places=3, default=0.000
    )
    specific_boil_grav = models.DecimalField(
        max_digits=5, decimal_places=3, default=0.000
    )
    pre_boil_vol = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00
    )
    post_boil_vol = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00
    )
    fermentation_temp = models.DecimalField(
        max_digits=4, decimal_places=1, default=0.0
    )


    def __str__(self):
        return self.memo












######### end of file ############
