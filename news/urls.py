from django.urls import path
from . import views

urlpatterns = [
    path('', views.process_query, name = "process_query"),
    path('favourite/', views.find_favourite, name = "favourite"),
    path('create/',views.create_user,name='user')

]