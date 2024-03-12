from django.urls import path
from .views import ForumQuestionList, ForumQuestionDetail, ForumAnswerList, ForumAnswerDetail, ForumAnswerLike, ForumQuestionLike

urlpatterns = [
    path('questions/', ForumQuestionList.as_view(), name='question-list'),
    path('questions/<int:pk>/', ForumQuestionDetail.as_view(), name='question-detail'),
    path('questions/<int:pk>/like/', ForumQuestionLike.as_view(), name='answer-like'),
    path('answers/', ForumAnswerList.as_view(), name='answer-create'),
    path('answers/<int:pk>/', ForumAnswerDetail.as_view(), name='answer-detail'),
    path('answers/<int:pk>/like/', ForumAnswerLike.as_view(), name='answer-like'),
]