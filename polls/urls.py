from django.contrib.auth.decorators import login_required
from django.urls import path


from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('landing/', views.landing, name='landing'),
    path('pickCat/', login_required(views.CategoryListView.as_view()), name="category"),
    path('category/<int:pk>', login_required(views.QuestionListView.as_view()), name='questionList'),
    path('question/<int:pk>', login_required(views.DetailView.as_view()), name='detail'),
   	path('results/<int:pk>', login_required(views.ResultsView.as_view()), name='results'),
   	path('<int:question_id>/vote/', views.vote, name='vote'),
   	path('signOn/', views.signOn, name='signOn'),
   	path('signout/', views.signout, name='signout'),


    ]
