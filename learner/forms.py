from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Deck, Card


class DeckForm(ModelForm):
	class Meta:
		model=Deck
		fields = ['name', 'description']
		
class CardForm(ModelForm):
	class Meta:
		model = Card
		fields = ['question', 'answer', 'sentence']

class JoinForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'size': '30'}))
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
        help_texts = {'username': None}

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    

