from django.urls import path
from django.contrib.auth import views as auth_views
from . import views # my views

urlpatterns = [
    path("signup/", views.signup, name="signup"), #old working code
    path("", views.home, name="home"),
    path('results/', views.results_table, name='results'),
    # path('your_submission/', views.dynamic_submission_view, name = 'dynamic_submission'),

    path("submission/", views.submission, name='submission')
]