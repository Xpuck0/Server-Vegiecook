from django.urls import path
from .views import CategoryListView, CategoryDetailView, CategoryCreateView 


urlpatterns = [
    path('<int:pk>', CategoryDetailView.as_view(), name='comment-detail'),
    path('create', CategoryCreateView.as_view(), name='comment-create'),
    path('', CategoryListView.as_view(), name='all-comments'),
]