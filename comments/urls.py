from django.urls import path
from .views import CommentDetailView, CommentCreateView, CommentListView 


urlpatterns = [
    path('<int:pk>', CommentDetailView.as_view(), name='comment-detail'),
    path('create', CommentCreateView.as_view(), name='comment-create'),
    path('', CommentListView.as_view(), name='all-comments'),
]

