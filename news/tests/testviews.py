import json
from typing_extensions import ParamSpecArgs
from django.test import TestCase, Client
from django.test.client import JSON_CONTENT_TYPE_RE
from django.urls import reverse
from news.models import Query , QueryResult , User, User_Favourite_Article
from django.http import JsonResponse
import datetime

# Create your tests here.

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.process_query_url = reverse('process_query')
        self.find_favourite_url = reverse('favourite')
        self.create_user_url = reverse('user')

        #creating a dummy user by the name mpopatia
        self.dummy_user = User.objects.create(
                name = 'mpopatia')

        #making a dummy query
        self.dummy_query = self.client.get(self.process_query_url, {'query':"test"})
        
        #saving a dummy article id to test 'favourites/' URL
        self.dummy_article_id= QueryResult.objects.all()[:1].get().get_query_result_id()

    def test_create_user_with_no_username(self):
        """Testing if API return a 400 Bad Request response if no username is provided to create a user
        """
        response = self.client.post(self.create_user_url)
        self.assertEquals(response.status_code, 400)

    def test_create_user_with_existing_username(self):
        """Testing if API can handle if a new user is being created with an existing username
        """
        response = self.client.post(self.create_user_url,**{'QUERY_STRING':'user=mpopatia'})
        self.assertEquals(response.status_code, 403)


    def test_get_request_to_create_user(self):
        """Testing if API return a 404 Not Found response if GET request instead of POST
        """
        response = self.client.get(self.create_user_url)
        self.assertEquals(response.status_code, 404)

    def test_news_reponse_always_in_json(self):
        """Testing if the API response is always in json format for "news/" URL
        """
        response = self.client.get(self.process_query_url)
        self.assertEquals(type(response), JsonResponse)

    def test_favourite_reponse_always_in_json(self):
        """Testing if the API response is always in json format for "favourite/" URL
        """
        response = self.client.get(self.find_favourite_url)
        self.assertEquals(type(response), JsonResponse)

    def test_news_without_keyword(self):
        """Testing if API return a 200 OK response if no keyword is provided
        """
        response = self.client.get(self.process_query_url)
        self.assertEquals(response.status_code, 200)

    def test_news_with_keyword(self):
        """Testing if API return a 200 OK response if a keyword is provided
        """
        response = self.client.get(self.process_query_url, {'query':"bitcoin"})
        self.assertEquals(response.status_code, 200)

    def test_if_repeated_query_fetched_from_db(self):
        """Testing if a repeated query is fetched from existing database instead of making a new request.
        it is proved if the time stamp of first and repeated query is same.
        """
        Query.objects.create(keyword = 'bitcoin')
        search_time = Query.objects.get(keyword = 'bitcoin').query_time
        response = self.client.get(self.process_query_url, {'query':"bitcoin"})
        new_search_time = Query.objects.get(keyword = 'bitcoin').query_time
        self.assertEquals(search_time, new_search_time)

    def test_repeated_query_after_expiry(self):
        """Testing if query is repeated but after expiry time, the API makes a new request to thiedparty news APIs instead
        of fetching old query results from the database.

        To do this a dummy time is created tby subtracting expiry time(120s) from current time and a query is posted with dummy time.
        and if the time stamp on repeated query result and dummy time are differnet it means a new request is sent.
        """

        dummy_time=datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=120)
        Query.objects.create(keyword = 'bitcoin',query_time=dummy_time)
        response = self.client.get(self.process_query_url, {'query':"bitcoin"})
        search_time = Query.objects.get(keyword = 'bitcoin').query_time
        self.assertNotEquals(dummy_time, search_time)

    def test_favourites_without_username(self):
        """Testing if fetch favourites request is handled by the API if a username is not mentioned.
        """

        response = self.client.get(self.find_favourite_url)
        self.assertEquals(response.status_code, 404)

    def test_favourites_with_non_existing_username(self):
        """Testing if fetch favourites request is handled by the API if a username is mentioned but a user is not 
        created by that username
        """
        
        response = self.client.get(self.find_favourite_url)
        self.assertEquals(response.status_code, 404)

    def test_favourites_with_existing_username(self):
        """Testing if API returns a success response in returning a fetch favoruite query for a user
        """
        
        response = self.client.get(self.find_favourite_url,{'user':'mpopatia'})
        self.assertEquals(response.status_code, 200)

    def test_favourite_get_request_including_article_id(self):
        """Testing if a GET request is used instead of POST request to add or remove an article from favourites
        """
        response = self.client.get(self.find_favourite_url,{'user':'mpopatia','id':2506})
        self.assertEquals(response.status_code, 400)

    def test_favourite_with_invalid_id(self):
        """Testing if an invalid article id is passed to add or romove from favourites. 
        invalid means that a article does not existing with that aricle id
        """
        response = self.client.post(self.find_favourite_url,**{'QUERY_STRING':'user=mpopatia&id=42144'})
        self.assertEquals(response.status_code, 404)

    def test_favourite_with_valid_id(self):
        """Testing if a valid article id is passed to add or romove from favourites. 
        valid means that a article exists with that aricle id
        """

        response = self.client.post(self.find_favourite_url,**{'QUERY_STRING':'user=mpopatia&id='+str(self.dummy_article_id)})
        self.assertEquals(response.status_code, 200)





    



    


    



    
        
