import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

class QuesionModelTests(TestCase):

	def test_was_published_recently_with_future_question(self):
		"""
		checks to see if was_published_recently() returns false
		for questions with a future publish_date attribute
		"""
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(publish_date=time)
		self.assertIs(future_question.was_published_recently(), False)

	def test_was_published_recently_with_old_question(self):
		"""
		checks to see if was_published_recently() returns false
		for questions with a future publish_date attribute
		"""
		time = timezone.now() - datetime.timedelta(days=30)
		future_question = Question(publish_date=time)
		self.assertIs(future_question.was_published_recently(), False)
		
	def test_was_published_recently_with_recent_question(self):	
		"""
		checks to see if was_published_recently() returns false
		for questions with a future publish_date attribute
		"""
		time = timezone.now() - datetime.timedelta(hours=10)
		future_question = Question(publish_date=time)
		self.assertIs(future_question.was_published_recently(), True)
		
class QuestionIndexViewTests(TestCase):
	
	def test_no_questions(self):
		#check appropriate response for no questions
		response = self.client.get(reverse('polls:index'))
		self.assertEquals(response.status_code, 200)
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'],[])
		
	def test_past_question(self):
		#check past questions are shown
		create_question(question_text="Test question", days=-20)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: Test question>']
		)
		
	def test_future_question(self):
		#future questions aren't shown until after their publish date
		create_question(question_text="its gonna be the future soon", days=358)
		response = self.client.get(reverse('polls:index'))
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'],[])

	def test_future_question_and_past_question(self):
		#display past questions, but not future
		create_question(question_text="Past", days=-30)
		create_question(question_text="Future", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: Past>']
		)

	def test_two_past_questions(self):
		#checking that multiple questions are returned
		create_question(question_text="long ago", days=-96)
		create_question(question_text="even longer ago", days=-100)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: long ago>', '<Question: even longer ago>']
		)
        
class QuestionDetailViewTests(TestCase):
	def test_future_question(self):
		#trying to view a future question triggers 404
		future_question = create_question(question_text='not just yet', days=100)
		url = reverse('polls:detail', args=(future_question.id,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)

	def test_past_question(self):
		#a past question should be displayed when going to the detail page
		past_question = create_question(question_text='come and gone', days=-5)
		url = reverse('polls:detail', args=(past_question.id,))
		response = self.client.get(url)
		self.assertContains(response, past_question.question_text)        

def create_question(question_text, days):
	#creates a question given the question text and day modifier
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, publish_date=time)