from django.urls import path
from replies.views import ReplyCreateView, ReplyDetailView

urlpatterns = [
    path('create', ReplyCreateView.as_view(), name='reply-create'),
    path('<int:pk>', ReplyDetailView.as_view(), name='reply-detail')
    # path('', )
]
