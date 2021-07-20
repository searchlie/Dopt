from django.urls import path
from . import views

urlpatterns = [
   
    path("", views.Dopt_view, name="new"),
    path("csv_download", views.file_download_view, name="file_download_view"),

]