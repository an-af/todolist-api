import json
from django.http import JsonResponse
import datetime
from .  models import Task

def testing(request):
    time = datetime.datetime.now()
    try:
        response = {"msg" : "OK",
                    "time" : time.strftime("%d-%m-%y")
                    }
        return JsonResponse(response, status=200)
    except Exception as error:
        response = {"msg" : str(error)}
        return JsonResponse(response, status=500)

# Task 

def allTask(request):
    data = Task.objects.all().values('id','title','description', 'due_date', 'created_at', 'updated_at', 'category')
    time = datetime.datetime.now()
    try:
        response = {"data" : list(data),
                    "time" : time.strftime("%d-%m-%y")
                    }
        return JsonResponse(response, status=200)
    except Exception as error:
        response = {"msg" : str(error)}
        return JsonResponse(response, status=500)
    

