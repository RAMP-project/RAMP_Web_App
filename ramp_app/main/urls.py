from django.urls import path
from . import views

urlpatterns = [
    path("input/", views.input, name="ramp_input"),
    path("", views.start, name="ramp_start"),
    path("start/", views.start, name="ramp_start"),
    path("result/", views.result, name="ramp_result"),
    path("download/", views.download, name="ramp_download_excel"),
    path("save/", views.save, name="ramp_save"),
    path("saved_profiles/", views.saved_profiles, name="saved_profiles")
    ]