from django.urls import path
from .views import ForumQuestionList, ForumQuestionDetail, ForumAnswerList, ForumAnswerDetail, ForumAnswerLike, ForumQuestionLike, LikeDetail, CheckLikeAPIView

urlpatterns = [
    path('questions/', ForumQuestionList.as_view(), name='question-list'),
    path('questions/<int:pk>/', ForumQuestionDetail.as_view(), name='question-detail'),
    path('questions/<int:pk>/like/', ForumQuestionLike.as_view(), name='answer-like'),
    path('answers/', ForumAnswerList.as_view(), name='answer-create'),
    path('answers/<int:pk>/', ForumAnswerDetail.as_view(), name='answer-detail'),
    path('answers/<int:pk>/like/', ForumAnswerLike.as_view(), name='answer-like'),
    path('likes/<int:pk>/', LikeDetail.as_view(), name='like-detail'),
    path('likes/check/', CheckLikeAPIView.as_view(), name='check-like')
]