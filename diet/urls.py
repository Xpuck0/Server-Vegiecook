from django.urls import path
from .views import DietListCreate, DietDetail

urlpatterns = [
    path('', DietListCreate.as_view(), name='diet-list-create'),
    path('<int:pk>/', DietDetail.as_view(), name='diet-detail'),
]
