from django.urls import path

from .views import (
    CleaningView,
    CreateCollectionView,
    DatasetInit,
    FetchDataView,
    LinkingView,
    SGPCInfoView,
    SGPInfoView,
    UploadToCollectionView,
)

urlpatterns = [
    # parameterized ... has urlparams
    # unique ... fetched by only one svelte page
    # multiple ... fetched by multiple svelte-pages (branches accordingly)

    # create new sgproject, [unique]
    # path('create-sgproject', CreateProjectView.as_view()),
    # path('create-sgproject', ProjectView.as_view()),

    path('create-collection', CreateCollectionView.as_view()),

    path('upload-datasets-to-collection', UploadToCollectionView.as_view()),

    path('fetch-datasets-from-collection', FetchDataView.as_view()),

    # path('tools-workflow-info', ToolView.as_view()),

    # saves datasets, - datasetentries and attaches them to specific sgproject
    # at the moment [unique, parameterized]
    # path('datasetupload', DataUploadView.as_view()),

    # on post: creates init step in sgproject and saves actions
    # [unique, parameterized]
    path('datasets_init', DatasetInit.as_view()),

    # on get: not implemented yet (might be merged later)
    # on post: initiates cleaning on datasets, creates new dataset-versions
    # at the moment [unique, parameterized]
    path('apply_cleaning', CleaningView.as_view()),

    # on get: not implemented yet (might be merged later)
    # on post: initiates linking on datasets, creates new dataset-versions
    # at the moment [unique, parameterized]
    path('apply_linking', LinkingView.as_view()),

    path('all-sgp-info', SGPInfoView.as_view()),

    path('all-sgpc-info', SGPCInfoView.as_view()),
    # returns dataset data etc. for specific sgproject
    # this might be a good one to merge into
    # [multiple, parameterized]
    # path('datasets_data', DatasetDataView.as_view()),


    # path('history', ProjectHistoryView.as_view()),
]
