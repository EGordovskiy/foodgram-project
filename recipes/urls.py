from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_ingredients, name='add_ingredients'),
    path('new/', views.new_recipe, name='new_recipe'),
    path('purchases/', views.purchases_list, name='purchases_list'),
    path('<username>/', views.profile, name='profile'),
    path('<username>/<int:recipe_id>/', views.recipe_view, name='recipe_view'),
    path('<username>/<int:recipe_id>/edit/', views.recipe_edit, name='recipe_edit'),
]