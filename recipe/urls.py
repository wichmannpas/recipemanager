from django.urls import path

from . import views

app_name = 'recipe'
urlpatterns = [
    path('', views.list_recipes, name='list_recipes'),
    path('<int:pk>/', views.view_recipe, name='view_recipe'),
]
