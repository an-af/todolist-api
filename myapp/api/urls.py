from django.urls import path
from . import views

urlpatterns = {
    # test
    path('test', views.testing, name="testing"),
    
    # task
    path('task', views.allTask, name="allTask"),
    path('task/<int:taskId>', views.getTaskById, name="getTaskById"),
    
    # category
    path('category', views.allCategory, name="allCategory"),
    path('category/<int:categoryId>', views.getCategoryById, name="getCategoryById"),
}