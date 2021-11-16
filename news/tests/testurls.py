from django.test import SimpleTestCase
from django.urls import reverse, resolve
from news.views import process_query,find_favourite,create_user

class TestUrls(SimpleTestCase):

    def test_process_query_url_resolves(self):
        """Testing if the 'news/' url resolves and returns the process_query function from views
        """
        url = reverse('process_query')
        self.assertEquals(resolve(url).func, process_query)

    def test_process_query_url_resolves(self):
        """Testing if the 'favourite/' url resolves and returns the find_favourite function from views
        """
        url = reverse('favourite')
        self.assertEquals(resolve(url).func, find_favourite)

    def test_process_query_url_resolves(self):
        """Testing if the 'create/' url resolves and returns the create_user function from views
        """
        url = reverse('user')
        self.assertEquals(resolve(url).func, create_user)

    
