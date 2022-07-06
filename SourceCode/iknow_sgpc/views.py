from django.http import JsonResponse

from .models import SGPC
from .serializer import CreateCollectionSerializer

# creates entry in SGPC
# expects a dict in data with 'data' : {..} and optional subkeys:
# bioprojectname, collectionname, description
# everything else will be ignored or results in error message and nothing happening


def createCollection(request):
    data: dict = request.data

    if type(data) == dict and 'data' in data.keys():
        serializer = CreateCollectionSerializer(data=data['data'])

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"project_id": serializer.data['id']})
        else:
            return JsonResponse({"msg": "error"})
    else:
        return JsonResponse({"msg": "error"})


def get_all_sgp_info():
    info = [['Collectionname', 'Bioprojectname', 'Source dataset']]
    for sgpc in SGPC.objects.all():
        for sgp in sgpc.associated_sgprojects.all():
            info.append([sgpc.collectionname, sgp.bioprojectname, sgp.source_dataset.all()[0].file_field.name])

    return info


def get_all_sgpc_info():
    info = [['Collectionname', 'Bioprojectname', '# associated graphs']]

    for sgpc in SGPC.objects.all():
        info.append([sgpc.collectionname, sgpc.bioprojectname, len(sgpc.associated_sgprojects.all())])

    return info
