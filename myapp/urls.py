from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # path("home/", views.home, name="home"), #optional but a little helpful
    path("result/", views.result, name="result"),
    path("submission/", views.submission, name="submission")
]