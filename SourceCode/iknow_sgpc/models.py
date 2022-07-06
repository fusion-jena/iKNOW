# from django.conf import settings
from django.db import models

from planthub.iknow_sgp.models import SGP

# Create your models here.

# https://www.tutorialspoint.com/adding-json-field-in-django-models
# https://riptutorial.com/django/example/30649/foreignkey
# https://stackoverflow.com/questions/34305805/foreignkey-user-in-models

# TODO: make own field and give client the possibility to create new bioprojectname
BIOPROJECTNAME_CHOICES = [
    ('PhenObs', 'Phenobs'),
    ('Glonaf', 'Glonaf'),
    ('sPlot', 'sPlot')
]


class SGPC(models.Model):
    # name of this collection (user convenience when continuing work)
    collectionname = models.CharField(max_length=255, default='')

    # name of the associated biology research project (same for the associated sgps)
    bioprojectname = models.CharField(max_length=255, choices=BIOPROJECTNAME_CHOICES, default='PhenObs')

    # description of the collection (user convenience)
    description = models.CharField(max_length=2000, default='')

    # all associated sgprojects (should be only assigned once and not changed afterwards)
    associated_sgprojects = models.ManyToManyField(SGP)

    # later for access control and displaying user specific database entries etc.
    # owningUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=1)

    # STEPS TO ADD A FIELD:

    # 1. add field here
    # add field in serializer
    # name field in frontend correctly
    # python manage.py makemigrations
    # python manage.py migrate
