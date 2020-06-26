from django.urls import path
from . import views
urlpatterns = [
    path('', views.Home,name="Home"),
    path('delete/<city_name>', views.delete_city,name="delete_city"),

]