import re
from django.db.models import query
from django.shortcuts import render
from .apifunction import get_news
from django.http import JsonResponse
from django.conf import settings
import pytz ,datetime
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F

from .models import Query , QueryResult , User, User_Favourite_Article

# Create your views here.

EXPIRY_TIME = settings.EXPIRY_TIME

def add_to_db(obj,keyword):
    """when called, it creates an object in the db model for the article called via searched keyword. 

    Args:
        obj : main object to connect added data with.
        keyword (str): searched keyword in the third party API.
    """    
    
    results=get_news(keyword)

    for result in results:
        new = QueryResult.objects.create( headline = result["headline"], link = result["link"], source = result["source"] )
        obj.query_result.add(new)
    

@csrf_exempt
def process_query(request):
    """the function is called upon "news/" URL. it processes the query and calls the apifunction to fetch news articles 
    from third party news APIs. 

    If a query is new, it makes a fresh request to third party APIs and returns the query results and adds the
    query and query results into the database.
    Otehrwise, if the query is repeated, it fetches the results from the database; if it has not passed the expiry time( set to 120s).
    If it has passed the expiry team a new request is sent to the third party news APIs and the results are updated in the database.

    Args:
        request (GET)

    Returns:
        json: returns the list of query results in the form of json object.
    """    

    if request.method =='POST':
        return JsonResponse({'Response': 'Invalid Request type, please use "GET"'}, status=400)

    try:
        
        keyword = request.GET.get('query')
        request_time = datetime.datetime.now(pytz.UTC)

        obj, created = Query.objects.get_or_create(
            keyword = keyword
        )

        if created==True:
            add_to_db(obj,keyword)
        
        elif (request_time - obj.query_time).seconds  > EXPIRY_TIME:

            obj.query_result.all().delete()
            Query.objects.filter(keyword = keyword).update(query_time = request_time)

            add_to_db(obj,keyword)

        response=[]
        for item in obj.query_result.all():
            response.append(item.to_dict())

        return JsonResponse(response, safe = False, status=200)

    except Exception as e:
        print(e)
        return JsonResponse({'Response': 'Something went wrong'}, status=400)

@csrf_exempt 
def find_favourite(request):
    """
    this function is called upon "favourite/" URL.
    
    on a "GET" request, client provides a username for which the function returns all the favoutite articles of the 
    particular user sorted by latest favourite article first.

    on a "POST" request, client provides a username and an id of an article he/she wants to add in favourites 
    or remove from favourites.


    Args:
        request (GET/POST)

    Returns:
        GET:
            json: returns a list of favourite articles of provided username.
        POST:
            json: returns the details of the article, with a "favoruite" key that determines of an article is added(True) or removed (False)
            from favourite list of the user.
    """    
    
    try:
        if request.method =='GET':
            username = request.GET.get('user')
            news_id = request.GET.get('id')
            if news_id != None:
                return JsonResponse({'Response': 'Invalid Request'}, status=400)

            try:
                user_id=User.objects.get(
                    name=username).get_user_id()
            except:
                return JsonResponse({'response': 'user not found'}, status=404)

            response=[]

            articles=User_Favourite_Article.objects.filter(
                user=user_id).order_by(F('time_added').desc())

            for item in articles:
                response.append(item.to_dict())
                

            return JsonResponse(response, safe = False, status=200)

        else:
            username = request.GET.get('user')
            news_id = request.GET.get('id')

            try:
                user_id=User.objects.get(
                    name=username).get_user_id()
            except:
                return JsonResponse({'response': 'user not found'},status=404)

            try:
                check=QueryResult.objects.get(id=news_id)
            except:
                return JsonResponse({'Response': 'Article id not found'}, status=404)

            result={'user':username}
            fav_obj , created = User_Favourite_Article.objects.get_or_create(user_id=user_id,article_id=news_id)
            fav_id=fav_obj.id
            result['favourite'] = created
            output=QueryResult.objects.get(id=news_id).to_dict()
            response=[{**result, **output}]
            if created == False:
                User_Favourite_Article.objects.get(id=fav_id).delete()

            return JsonResponse(response, safe = False, status=200)
            

    except Exception as e:
        print(e)
        return JsonResponse({'Response': 'Invalid Request'}, status=400)
        

@csrf_exempt
def create_user(request):
    """this function is called upon "create/" URL.
    creates a new user in the database.

    Args:
        request (POST): a username is provided by the client.

    Returns:
        json: returns a response to the client, notifying whether a new user is created.
    """    
    try:
        if request.method== 'POST':
            username = request.GET.get('user')
            if username ==None:
                return JsonResponse({'Response': 'please enter a user name'}, status=400)

            obj, created = User.objects.get_or_create(
                name = username)

            if created == False:
                return JsonResponse({'Response': 'username already in use'}, status=403)
            else:
                return JsonResponse({'Response': 'news user created: '+str(username)}, status=201)
        else:
            return JsonResponse({'Response': 'Invalid Request Type, please use "POST"'}, status=404)            

    except Exception as e:
        print(e)
        return JsonResponse({'Response': 'Invalid URL'}, status=404)
