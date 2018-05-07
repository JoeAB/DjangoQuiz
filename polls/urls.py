from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('category/<int:pk>', views.QuestionListView.as_view(), name='questionList'),
    path('question/<int:pk>', views.DetailView.as_view(), name='detail'),
   	path('results/<int:pk>', views.ResultsView.as_view(), name='results'),
   	path('<int:question_id>/vote/', views.vote, name='vote'),
    ]
