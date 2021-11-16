from django.db import models
from django.db.models.fields.related import ManyToManyField
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.

class QueryResult(models.Model):    
    headline=models.CharField(max_length=1500)
    link = models.URLField()
    source= models.CharField(max_length=10)

    def to_dict(self):
        """creates a dictionary of the objects from the model.

        Returns:
            dict: returns model data in the form of a dictionary.
        """        

        dt={
            "id":self.id,
            "headline": self.headline,
            "link": self.link,
            "source": self.source}

        return dt

    def get_query_result_id(self):
        
        return self.id
    
class Query(models.Model):
    keyword=models.CharField(max_length=50, null=True)
    query_time=models.DateTimeField(auto_now_add=True)
    query_result= models.ManyToManyField(QueryResult)

class User(AbstractBaseUser):
    name = models.CharField(max_length=50)

    def get_user_id(self):
        
        return self.id


class User_Favourite_Article(models.Model):
    time_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    article  = models.ForeignKey(QueryResult,on_delete=models.CASCADE)

    def to_dict(self):
        """creates a dictionary of the objects from the model.

        Returns:
            dict: returns model data in the form of a dcitionary.
        """

        dt={
            "id":self.article.id,
            "headline": self.article.headline,
            "link": self.article.link,
            "source": self.article.source
        }
        return dt





    