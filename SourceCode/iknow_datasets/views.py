# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.http import JsonResponse
import os
from pathlib import Path

from django.conf import settings
from django.core.files import File

from .models import Dataset

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
STORAGE_DIR = f"{settings.MEDIA_ROOT}/iknow_datasets_temp/"


def handle_uploaded_file(file, filename):
    # TODO:
    #   - error handling

    # create the model instance
    datasetentry = Dataset()

    # pathlib seems to be the way to handle paths across all OS
    path = Path(f"{STORAGE_DIR}00_{filename}")

    # write the file
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    # open the just written file to save it to the file_field
    with open(path, 'rb') as doc_file:
        datasetentry.file_field.save(filename, File(doc_file), save=True)

    # save the instance
    datasetentry.save()

    return datasetentry
