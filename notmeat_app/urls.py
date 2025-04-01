from django.urls import path

from notmeat_app import views


urlpatterns = [path("", views.index, name="index")]
