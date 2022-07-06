from rest_framework import serializers

from .models import SGPC


class CreateCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SGPC
        fields = ['id', 'bioprojectname', 'description', 'collectionname']
