from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("randomEntry/", views.randomEntry, name="randomEntry"),
    path("editEntry/<str:entry>/", views.editEntry, name="editEntry"),
    path("<str:entry>/", views.entry, name="entry")
]
