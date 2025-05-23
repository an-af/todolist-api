import json
from django.http import JsonResponse
import datetime
from .  models import Task, Category
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt


# -- Testing --
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

# -- Task --

def allTask(request):
    data = Task.objects.all().values('id','title','description', 'due_date', 'created_at', 'updated_at', 'category__id', 'category__name', 'category__description')
    time = datetime.datetime.now()
    # created formated data
    formated_data = []
    for item in data:
        formated_data.append({
            'id' : item['id'],
            'title' : item['title'],
            'description' : item['description'],
            "due_date"  : item["due_date"].isoformat() if item["due_date"]  else None,
            "created_at"  : item["created_at"].isoformat(),
            "updated_at" : item["updated_at"].isoformat(),
            "category" : {
                "id" : item["category__id"],
                "name" : item["category__name"],
                "description" : item["category__description"]
            }
        })
    try:
        response = {"data" : formated_data,
                    "time" : time.strftime("%d-%m-%y | %H:%M")
                    }
        return JsonResponse(response, status=200)
    except Exception as error:
        response = {"msg" : str(error)}
        return JsonResponse(response, status=500)

@csrf_exempt   
def getTaskById(request, taskId):
    try:

        # get data by id
        if request.method == 'GET':
            data = Task.objects.get(id = taskId)
            # convert dictionary
            data = model_to_dict(data)
            # category
            category_data = Category.objects.get(id = data['category'])
            category_data = model_to_dict(category_data)

            # formating data
            formated_data = {
                'id' : data['id'],
                'title' : data['title'],
                'description' : data['description'],
                "due_date"  : data["due_date"].isoformat() if data["due_date"]  else None,
                # "created_at"  : data["created_at"].isoformat(),
                # "updated_at" : data["updated_at"].isoformat(),
                "category" : {
                    "id" : category_data["id"],
                    "name" : category_data["name"],
                    "description" : category_data["description"]
                }
            }

            response = {"data" : formated_data}
            return JsonResponse(response, status = 200)
        
        # delete data by id
        if request.method == 'DELETE':
            data = Task.objects.get(id = taskId)
            data.delete()
            response = {"msg" : "data delete success !"}
            return JsonResponse(response, status = 200)
    
    # object not found exception
    except ObjectDoesNotExist as error:
        response = {"error" : str(error)+" please try again.."}
        return JsonResponse(response, status = 404)
    
    # another error from server
    except Exception as error:
        response = {"error" : str(error)}
        return JsonResponse(response, status = 500)

# -- Category --

def allCategory(request):
    try:
        date = datetime.datetime.now()
        dateFormat = date.strftime("%d-%m-%Y")
        data = Category.objects.all().values('name', 'description')
        response = {
            "time" : dateFormat,
            "data" : list(data)
        }
        return JsonResponse(response, status = 200)
    except Exception as msg:
        response = {
            "datetime" : dateFormat,
            "error" : str(msg),
        }
        return JsonResponse(response, status = 500)
    
def getCategoryById(request, categoryId):
    try:
        response = {"msg" : "getCategoryByID() ok ", "id" : categoryId}
        return JsonResponse(response, status = 200)
    except Exception as error:
        response = {"msg" : str(error)}
        return JsonResponse(response, status = 500)