from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Category, Choice, Question


def index(request):

	return render(request, 'polls/index.html')


class CategoryListView(generic.ListView):
	template_name = 'polls/category.html'
	context_object_name = 'category_list'
	
	def get_queryset(self):
		return Category.objects.order_by('category_name')

class QuestionListView(generic.ListView):
	template_name = 'polls/questionList.html'
	context_object_name = 'latest_question_list'
	
	def get_queryset(self):
		#get five most recent, but none in the future
		return Question.objects.filter(publish_date__lte=timezone.now()).order_by('-publish_date')[:5]
    
class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'
	
	def get_queryset(self):
		#don't allow future questions here
		return Question.objects.filter(publish_date__lte=timezone.now())
		
def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExit):
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice.",
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
		
class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'
	
def signOn(request):
	userNameParam = request.POST.get("userName", "")
	passwordParam = request.POST.get("password", "")
	
	user = authenticate(username=userNameParam, password=passwordParam)
	
	if user is not None:
		return HttpResponseRedirect(reverse('polls:landing'))
	else:
		return render(request, 'polls/index.html', 
		{'message': 'The username or password combination you have entered is incorrect.'})

def landing(request):
	return render(request, 'polls/landing.html')

