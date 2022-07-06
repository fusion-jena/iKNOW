import json
import os

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
# from iknow_tools.views import get_all_tools_workflow_info
from rest_framework.response import Response
# from distutils.log import error
# from django.db import models
# from django.shortcuts import render
from rest_framework.views import APIView

from planthub.iknow_datasets.models import Dataset
from planthub.iknow_datasets.views import handle_uploaded_file
from planthub.iknow_sgp.models import SGP
from planthub.iknow_sgp.views import createSGP
from planthub.iknow_sgpc.models import SGPC
from planthub.iknow_sgpc.views import (
    createCollection,
    get_all_sgp_info,
    get_all_sgpc_info,
)

# from .pdutil.pdconverter import append_boolean_list
from .pdutil.pdreader import (  # get_json_from_csv,; get_list_from_csv,
    get_list_from_csv_first10rows,
)

# from copyreg import constructor

jr_error = JsonResponse({"msg": "error"})

# everything about REQUEST HANDLING in django
# https://docs.djangoproject.com/en/4.0/ref/request-response/

# response error codes ... response codes für django rest_framework nachschauen und dann benutzen
# redirect ... goto und siehe svelte
# tool init


# TODO:
#   - implement testcontainers to run (cleaning/linking)
#   - reading and returning data of linking results (just as cleaningresult for now)
#   - implement rdf-ization for cleaned table data
#   - implement rdf-ization for linked table data
#   - undo functionality (just senseful naming of steps as a dropdown)

#   - check validity of each applied action
#   - return appropriate error codes for specific failures
#   - error handling etc. when client uploads files


# client creates new sgpc
class CreateCollectionView(APIView):
    def post(self, request):
        return createCollection(request)


# client uploads datasets into a sgpc
class UploadToCollectionView(APIView):
    def post(self, request):
        sgpc_pk = request.POST.get('sgpc_pk', default=None)

        if sgpc_pk is None:
            # sgpc_pk in request body not found
            print("sgpc_none error")
            return jr_error

        # get sgpc instance
        try:
            sgpc: SGPC = SGPC.objects.get(id=sgpc_pk)
        except ObjectDoesNotExist:
            # sgpc_pk was no valid primary key
            print("sgpc not_pk valid error")
            return jr_error

        # iterate over the files in the request
        for key, file in request.FILES.items():
            filename = request.FILES[key].name

            # let datasets create and return the instance
            new_dataset = handle_uploaded_file(request.FILES[key], filename)

            new_sgp = createSGP(sgpc.bioprojectname)
            new_sgp.source_dataset.add(new_dataset)

            # print("created new sgp with id: ", new_sgp.id)
            # print("adding sgp to sgpc: ", sgpc.pk)

            # add the datasets to the sgproject many2many field
            sgpc.associated_sgprojects.add(new_sgp)

        return JsonResponse({"msg": "success"})


# data from a specific sgpc is requested
class FetchDataView(APIView):
    def get(self, request):
        # get parameters from request
        sgpc_pk = request.GET.get('sgpc_pk', default=None)

        # get sgproject instance
        if sgpc_pk is None:
            # sgpc_pk in request body not found
            print("sgpc_none error")
            return jr_error

        # get sgpc istance
        try:
            sgpc: SGPC = SGPC.objects.get(id=sgpc_pk)
        except ObjectDoesNotExist:
            # sgpc_pk was no valid primary key
            print("sgpc_pk not valid error")
            return jr_error

        # client tells us what data about current files is req_uired
        req_names = False
        req_datasets = False
        if (request.GET.get('names', '') != ''):
            req_names = True

        if (request.GET.get('datasets', '') != ''):
            req_datasets = True

        data = self.prepare_datasets(sgpc, req_names, req_datasets)

        # print("returning prepared datasets: ", prepared_datasets)
        response = JsonResponse(data, safe=False)

        return response

    def prepare_datasets(self, sgpc: SGPC, req_names: bool, req_datasets: bool):
        prepared_datasets = {}

        for i, sgp in enumerate(sgpc.associated_sgprojects.all()):
            # print("sgp.id: ", sgp.id, " sgp.bioprojectname: ", sgp.bioprojectname)
            dataset = self.get_latest_dataset_from_SGP(sgp)
            helper = {}
            helper["sgp_pk"] = sgp.pk

            if req_names:
                print("loaded filename")
                helper["filename"] = os.path.basename(dataset.file_field.name)
            if req_datasets:
                print("loaded dataset")
                helper["dataset"] = self.loadTableData(dataset)

            prepared_datasets[i] = helper

        return prepared_datasets

    # depending on the last phase type in each sgp, this
    # function returns the latest dataset object in the sgp
    def get_latest_dataset_from_SGP(self, sgp: SGP):
        # <= 1 ... INIT PHASE
        if len(sgp.provenanceRecord) <= 1:
            # print("The source dataset for sgp: ", sgp.pk, " is ", sgp.source_dataset.all()[0])
            return sgp.source_dataset.all()[0]
        else:
            last_phasetype = sgp.provenanceRecord[str(len(sgp.provenanceRecord)-1)]["type"]

            # CLEANING PHASE
            if last_phasetype == "cleaning":
                return sgp.source_dataset.all()[0]
            # LINKING PHASE
            elif last_phasetype == "linking":
                return sgp.source_dataset.all()[0]
            # ELSE
            else:
                return sgp.source_dataset.all()[0]

    def loadTableData(self, dataset_obj):

        lst = get_list_from_csv_first10rows(dataset_obj.file_field.path)
        # lst = append_boolean_list(lst)

        return lst


# sgp init phase, client chooses header mappings
class DatasetInit(APIView):
    # handles the submit from the projctinit page
    # this creates the first [key,value]-pair in the provenanceRecord of type="init"
    def post(self, request):
        data = json.loads(request.body)["requestdata"]

        sgpc_pk = data["sgpc_pk"]

        # get sgproject instance
        try:
            sgpc: SGPC = SGPC.objects.get(id=sgpc_pk)
        except ObjectDoesNotExist:
            # sgpc_pk was no valid primary key
            print("sgpc_pk not valid error")
            return jr_error

        for sgp in sgpc.associated_sgprojects.all():
            for key in data["tabledata"].keys():
                if data["tabledata"][key]["sgp_pk"] == sgp.pk:
                    if len(sgp.provenanceRecord) == 0:
                        self.safe_init_step(sgp, data["tabledata"][key])
                    else:
                        print("Error, trying to apply init phase to provenance record that is not empty.")

        response = JsonResponse({"success": "succesfully initialized"})

        return response

    def safe_init_step(self, sgp: SGP, data):
        sgp.provenanceRecord[0] = {}
        sgp.provenanceRecord[0]["type"] = "init"
        sgp.provenanceRecord[0]["selection"] = data["selection"]

        sgp.save()


# client invokes cleaning action
class CleaningView(APIView):

    # this is very experimental, and will change heavily
    # atm there is only the testmethod, which will not alter anything, but produce a new dataset version
    # any other method will just do nothing, and mark the output- the same as the input dataset in the record
    def post(self, request):
        json_data: dict = json.loads(request.body)["requestdata"]
        if "sgpc_pk" not in json_data.keys():
            return jr_error

        # Later -> grab sgpc here and look if these are the correct datasets/sgps
        # at the moment commented out because unused (flake8)

        # sgpc_pk = json_data["sgpc_pk"]

        # get sgpc istance
        # try:
        #     sgpc: SGPC = SGPC.objects.get(id=sgpc_pk)
        # except ObjectDoesNotExist:
        #     # sgpc_pk was no valid primary key
        #     print("sgpc not valid error")
        #     return jr_error

        # code runs AFTER CLEANING
        for i, key in enumerate(json_data["actions"]):
            # chosen cleaning method, (..= -1 means none)
            method = json_data['actions'][key]['method']

            # get sgp istance
            try:
                sgp: SGP = SGP.objects.get(id=key)
            except ObjectDoesNotExist:
                # sgp_pk was no valid primary key
                print("sgp not valid error")
                return jr_error

            latest_dataset: Dataset = self.get_latest_dataset_from_SGP(sgp)

            # ENTRY POINT CLEANING
            method, output_pk = self.handle_cleaning(latest_dataset.pk, method)

            self.append_cleaning_step(sgp, method, latest_dataset.pk, output_pk)

        return Response()

    # depending on the last phase type in each sgp, this
    # function returns the latest dataset object in the sgp
    def get_latest_dataset_from_SGP(self, sgp: SGP):
        # <= 1 ... INIT PHASE
        if len(sgp.provenanceRecord) <= 1:
            # print("The source dataset for sgp: ", sgp.pk, " is ", sgp.source_dataset.all()[0])
            return sgp.source_dataset.all()[0]
        else:
            last_phasetype = sgp.provenanceRecord[str(len(sgp.provenanceRecord)-1)]["type"]

            # CLEANING PHASE
            if last_phasetype == "cleaning":
                return sgp.source_dataset.all()[0]
            # LINKING PHASE
            elif last_phasetype == "linking":
                return sgp.source_dataset.all()[0]
            # ELSE
            else:
                return sgp.source_dataset.all()[0]

    def handle_cleaning(self, dataset_pk, method):
        if method == "-1":
            print(f"No cleaning was chosen for dataset with pk: {dataset_pk}")

            # [run tool]
            # run cmd line here
            # send response

            return "nocleaning", dataset_pk
        elif method == "0":
            print(f"Applying method 0 for dataset with pk: {dataset_pk}")
            return "testmethod", dataset_pk
        else:
            print(f"Not implemented yet, applying dummy cleaning step for dataset with pk: {dataset_pk}")
            return "dummy", dataset_pk

    def append_cleaning_step(self, sgp: SGP, method, d_pk_in, d_pk_out):
        cur_step = len(sgp.provenanceRecord)
        sgp.provenanceRecord[cur_step] = {}
        sgp.provenanceRecord[cur_step]["type"] = "cleaning"
        sgp.provenanceRecord[cur_step]["actions"] = {}
        sgp.provenanceRecord[cur_step]["actions"]["input"] = d_pk_in
        sgp.provenanceRecord[cur_step]["actions"]["output"] = d_pk_out
        sgp.provenanceRecord[cur_step]["actions"]["method"] = method

        sgp.save()


# client invokes linking action
class LinkingView(APIView):
    def post(self, request):
        json_data = json.loads(request.body)["requestdata"]
        if "sgpc_pk" not in json_data.keys():
            return jr_error

        # see identical comment on CleaningView

        # sgpc_pk = json_data["sgpc_pk"]

        # # get sgpc istance
        # try:
        #     sgpc: SGPC = SGPC.objects.get(id=sgpc_pk)
        # except:
        #     # sgpc_pk was no valid primary key
        #     print("sgpc not valid error")
        #     return jr_error

        for i, key in enumerate(json_data["actions"]):
            # chosen cleaning method, (..= -1 means none)
            method = json_data['actions'][key]['method']

            # get sgpc istance
            try:
                sgp: SGP = SGP.objects.get(id=key)
            except ObjectDoesNotExist:
                # sgp_pk was no valid primary key
                print("sgp not valid error")
                return jr_error

            latest_dataset: Dataset = self.get_latest_dataset_from_SGP(sgp)
            print(f"initializing linking method {method} for dataset with pk: {latest_dataset.pk}")

            method, output_pk = self.handle_linking(latest_dataset.pk, method)

        self.append_linking_step(sgp, method, latest_dataset.pk, output_pk)

        return Response()

    # depending on the last phase type in each sgp, this
    # function returns the latest dataset object in the sgp
    def get_latest_dataset_from_SGP(self, sgp: SGP):
        # <= 1 ... INIT PHASE
        if len(sgp.provenanceRecord) <= 1:
            # print("The source dataset for sgp: ", sgp.pk, " is ", sgp.source_dataset.all()[0])
            return sgp.source_dataset.all()[0]
        else:
            last_phasetype = sgp.provenanceRecord[str(len(sgp.provenanceRecord)-1)]["type"]

            # CLEANING PHASE
            if last_phasetype == "cleaning":
                return sgp.source_dataset.all()[0]
            # LINKING PHASE
            elif last_phasetype == "linking":
                return sgp.source_dataset.all()[0]
            # ELSE
            else:
                return sgp.source_dataset.all()[0]

    def handle_linking(self, dataset_pk, method):
        if method == "-1":
            print(f"No linking was chosen for dataset with pk: {dataset_pk}")
            return "nolinking", dataset_pk
        elif method == "5":
            print(f"Applying method 5 for dataset with pk: {dataset_pk}")
            return "testmethod", dataset_pk
        else:
            print(f"Not implemented yet, applying dummy linking step for dataset with pk: {dataset_pk}")
            return "dummy", dataset_pk

    def append_linking_step(self, sgp: SGP, method, d_pk_in, d_pk_out):
        cur_step = len(sgp.provenanceRecord)
        sgp.provenanceRecord[cur_step] = {}
        sgp.provenanceRecord[cur_step]["type"] = "linking"
        sgp.provenanceRecord[cur_step]["actions"] = {}
        sgp.provenanceRecord[cur_step]["actions"]["input"] = d_pk_in
        sgp.provenanceRecord[cur_step]["actions"]["output"] = d_pk_out
        sgp.provenanceRecord[cur_step]["actions"]["method"] = method

        sgp.save()


class SGPInfoView(APIView):
    def get(self, request):
        response = JsonResponse({"tabledata": get_all_sgp_info()})
        return response


class SGPCInfoView(APIView):
    def get(self, request):
        response = JsonResponse({"tabledata": get_all_sgpc_info()})
        return response
