# from django.shortcuts import render

from .models import SGP


def createSGP(bioprojectname: str):
    new_sgp = SGP()

    new_sgp.bioprojectname = bioprojectname

    new_sgp.save()

    return new_sgp
