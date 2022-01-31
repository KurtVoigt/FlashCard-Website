from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Deck(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	weight = models.DecimalField(max_digits=5, decimal_places=4)
	name = models.CharField(max_length=100, unique = True)
	description = models.CharField(max_length=700)


class Card(models.Model):
	deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
	question = models.CharField(max_length=100)
	answer = models.CharField(max_length=100)
	weight = models.DecimalField(max_digits=5, decimal_places=4)
	sentence = models.CharField(max_length=700)
	lastUpdatedDate = models.DateTimeField(auto_now=True, auto_now_add=False)
	
