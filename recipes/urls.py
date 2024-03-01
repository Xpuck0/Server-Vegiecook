from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import RecipeCreateView, RecipeListView, RecipeDetailView 

urlpatterns = [
    path('', RecipeListView.as_view(), name='recipe-list'),
    path('create', RecipeCreateView.as_view(), name='recipe-create'),
    path('<int:pk>', RecipeDetailView.as_view(), name='recipe-detail'),
] 
