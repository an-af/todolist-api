from django.urls import path
from . import views

urlpatterns = {
    path('test', views.testing, name="testing"),
    path('task', views.allTask, name="allTask")
}