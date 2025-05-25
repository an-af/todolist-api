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
@csrf_exempt
def allCategory(request):
    try:
        date = datetime.datetime.now()
        dateFormat = date.strftime("%d-%m-%Y | %H:%M WIB")

        # == GET METHOD ==
        if request.method == 'GET':
            data = Category.objects.all().values('name', 'description')
            response = {
                "time" : dateFormat,
                "data" : list(data)
            }

            return JsonResponse(response, status = 200)
        
        # == POST METHOD ==
        if request.method == 'POST':
            temp = json.loads(request.body.decode('utf-8'))
            newData = Category(**temp)
            newData.save()
            response = {
                "data" : temp,
                "server-time" : dateFormat
            }

            return JsonResponse(response, status = 200)
        
    except Exception as msg:
        response = {
            "datetime" : dateFormat,
            "error" : str(msg),
        }
        return JsonResponse(response, status = 500)
    

    
@csrf_exempt    
def getCategoryById(request, categoryId):
    try:
        date = datetime.datetime.now()
        dateFormat = date.strftime("%d-%m-%Y | %H:%M WIB")
        # -- Get Category --
        if request.method == 'GET':
            data = Category.objects.get(id = categoryId)
            data = model_to_dict(data)
            response = {"data" : data}
            return JsonResponse(response, status = 200)
        
        # -- del Category --
        if request.method == 'DELETE':
            data = Category.objects.get(id = categoryId)
            data.delete()
            response = {"msg" : "data success deleted !"}
            return JsonResponse(response, status = 200)
        
        # == PATCH category ==
        if request.method == 'PATCH':
            response = {
                "msg" : "Data updated !", 
                "server-time": dateFormat
            }
            data = Category.objects.get(id = categoryId)
            newData = json.loads(request.body.decode('UTF-8'))

            data.name = newData['name']
            data.description = newData['description']
            data.save()

            return JsonResponse(response, status = 200)

    except ObjectDoesNotExist as error:
        response = {"msg" : str(error)+"please try again..."}
        return JsonResponse(response, status = 404)
    except Exception as error:
        response = {"msg" : str(error)}
        return JsonResponse(response, status = 500)