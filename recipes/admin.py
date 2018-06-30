from django.contrib import admin

from . import models


class MashStepInline(admin.TabularInline):
    model = models.MashStep
    extra = 0


class HopInline(admin.TabularInline):
    model = models.Hop
    extra = 0


class FermentableInline(admin.TabularInline):
    model = models.Fermentable
    extra = 0


class MiscInline(admin.TabularInline):
    model = models.Miscellaneous
    extra = 0


class YeastInline(admin.TabularInline):
    model = models.Yeast
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    fieldsets = (
        ('RECIPE',
            {'fields': (('recipe_name', 'version', 'style'),)}
        ),
        ('BATCH',
            {'fields': (('batch_volume', 'og', 'abv'),)}
        ),
        ('TYPE',
            {'fields': (('brew_type', 'efficiency'),)}
        ),
        ('MASH',
            {'fields': (('strike_temp', 'strike_volume'),)}
        ),
        ('BOIL',
            {'fields': (('boil_time', 'boil_volume', 'boil_grav'),)}
        )
    )
    inlines = [
        MashStepInline,
        HopInline,
        FermentableInline,
        MiscInline,
        YeastInline
    ]


admin.site.register(models.Recipe, RecipeAdmin)
admin.site.register(models.MashStep)
admin.site.register(models.Hop)
admin.site.register(models.Fermentable)
admin.site.register(models.Miscellaneous)
admin.site.register(models.Yeast)
admin.site.register(models.Session)
