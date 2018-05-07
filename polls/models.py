import datetime

from django.db import models
from django.utils import timezone

class Category(models.Model):
	category_name = models.CharField('category name', max_length=50)

	def __str__(self):
		return self.category_name

class Question(models.Model):
	category = models.ForeignKey(Category, on_delete = models.CASCADE)
	question_text = models.CharField('question text', max_length=200)
	publish_date = models.DateTimeField('date published')
	
	
	def __str__(self):
		return self.question_text
		
	def was_published_recently(self):
		now = timezone.now()
		return timezone.now() - datetime.timedelta(days=1) <= self.publish_date <= now
	
class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete = models.CASCADE)
	choice_text = models.CharField('choice text', max_length=200)
	votes = models.IntegerField(default=0)
	
	def __str__(self):
		return self.choice_text
		

		
		