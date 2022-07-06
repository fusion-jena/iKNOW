# from django.conf import settings
from django.db import models

# import os


class Dataset(models.Model):
    #  General Info
    # owningUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=1)

    file_field = models.FileField(upload_to='iknow_datasets')
    # domainname = models.CharField(max_length=512)
