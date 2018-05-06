from django.shortcuts import render

# Create your views here.

from django.http import Http404
from django.shortcuts import render

from .models import Question

def index(request):
	latest_question_list = Question.objects.order_by('-publish_date')[:5]
	context = {'latest_question_list': latest_question_list}
	return render(request, 'polls/index.html', context)
    
def detail(request, question_id):
	try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404("A question with the selected ID does not exist.")
	return render(request, 'polls/detail.html', {'question': question})