from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from .forms import JoinForm, LoginForm, CardForm, DeckForm
from .models import Deck, Card
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import decimal
from django.utils import timezone

# Create your views here.

def index(request):
    return render(request, "index.html")

@login_required(login_url='learner:login') 
def dash(request):
	if request.user.is_authenticated:
		use = request.user
		decks = Deck.objects.filter(user = use)
		if(len(decks) < 1):
			pass
		else:
			#decay card weights based on amount of time that has passed
			now = timezone.now()
			for deck in decks:
				cards = Card.objects.filter(deck = deck)
				if(len(cards) < 1):
					continue
				for card in cards:
					num = decimal.Decimal(0.2)
					null = decimal.Decimal(0.0)
					dateArith = now - card.lastUpdatedDate
					hours = dateArith.seconds / 60 / 60
					if(hours < 24):
						continue
					while hours >= 24:
						card.weight = card.weight - num
						hours = hours - 24
					if(card.weight < null):
						card,weight = null
					#saving will automatically update the date to the present date
					card.save()
			
			
			#update deck weights
			for deck in decks:
				num = decimal.Decimal(0.0)
				cards = Card.objects.filter(deck = deck)
				if(len(cards) < 1):
					continue
				for card in cards:
					num = num + card.weight
				lengthh = decimal.Decimal(len(cards))
				deck.weight = (num/lengthh)
				deck.save()
		context = {
			"decks" : decks
		}
		return render(request, "dashboard.html", context)
	else:
		return redirect('learner:index')

@login_required(login_url='learner:login')		
def deck_delete(request, deckId):
	deck = Deck.objects.get(id=deckId)
	deck.delete()
	return redirect('learner:dashboard')
	
@login_required(login_url='learner:login')
def deck_add(request):
	if (request.method == "POST"):
		if ("add" in request.POST):
			add_form = DeckForm(request.POST)
			if (add_form.is_valid()):
				description = add_form.cleaned_data["description"]
				dName = add_form.cleaned_data["name"]
				user = User.objects.get(id=request.user.id)
				Deck(user=user, description=description, name=dName, weight=0.1).save()
				return redirect("learner:dashboard")
			else:
				context = {
					"form_data": add_form
				}
				return render(request, 'deckAdd.html', context)
		else:
		# Cancel
			return redirect("learner:dashboard")
	else:
		context = {
			"form_data": DeckForm()
		}
		return render(request, 'deckAdd.html', context)

@login_required(login_url='learner:login')
def card_add(request, deckId):
	if (request.method == "POST"):
		if ("add" in request.POST):
			add_form = CardForm(request.POST)
			if (add_form.is_valid()):
				deck = Deck.objects.get(id=deckId)
				question = add_form.cleaned_data["question"]
				answer = add_form.cleaned_data["answer"]
				sentence = add_form.cleaned_data["sentence"]
				Card(deck=deck, question=question, answer=answer, weight=0.1, sentence=sentence).save()
				return redirect("learner:dashboard")
			else:
				context = {
					"form_data": add_form
				}
				return render(request, 'cardAdd.html', context)
		else:
		# Cancel
			return redirect("learner:dashboard")
	else:
		context = {
			"form_data": CardForm()
		}
		return render(request, 'cardAdd.html', context)
		
@login_required(login_url='learner:login')
def deck_review(request, deckId):
	deck = Deck.objects.get(id = deckId)
	cDB = Card.objects.filter(deck=deck)
	cards = sorted(cDB, key = lambda x: x.weight)
	#check sorted length
	if(len(cards) < 1):
		return redirect("learner:dashboard")
	if(cards[0].weight != 1.0):
		context = {
			"deck": deck,
			"card": cards[0]
		}
		return render(request, 'reviewDeck.html', context)
	else:
		return redirect("learner:dashboard")

@login_required(login_url='learner:login')
def card_answer(request, deckId):
	deck = Deck.objects.get(id = deckId)
	cDB = Card.objects.filter(deck=deck)
	currentCard = sorted(cDB, key = lambda x: x.weight)[0]
	if (request.method == "POST"): 
		if ("great" in request.POST):
			d= decimal.Decimal(0.4)
			currentCard.weight = currentCard.weight + d
		if ("good" in request.POST):
			d= decimal.Decimal(0.2)
			currentCard.weight = currentCard.weight + d
		if ("neutral" in request.POST):
			d= decimal.Decimal(0.1)
			currentCard.weight = currentCard.weight + d
		if ("bad" in request.POST):
			d= decimal.Decimal(0.1)
			currentCard.weight = currentCard.weight - d
		if ("terrible" in request.POST):
			d= decimal.Decimal(0.2)
			currentCard.weight = currentCard.weight - d
			
		if(currentCard.weight > 1.0):
			currentCard.weight = 1.0
		if(currentCard.weight < 0.0):
			currentCard.weight = 0.0
		currentCard.save()
		return redirect("learner:deckReview", deckId = deckId)

	else:
		context = {
			"deck": deck,
			"card": currentCard
		}
		return render(request, "cardAnswer.html", context)
def join(request):
    if (request.method == "POST"):
        join_form = JoinForm(request.POST)
        if (join_form.is_valid()):
            # Save form data to DB
            user = join_form.save()
            # Encrypt the password
            user.set_password(user.password)
            # Save encrypted password to DB
            user.save()
            # Success! Redirect to home page.
            return redirect("learner:index")
        else:
            # Form invalid, print errors to console
            context = {"join_form": join_form}
            return render(request, 'join.html', context)
    else:
        join_form = JoinForm()
        page_data = {"join_form": join_form}
        return render(request, 'join.html', page_data)


def user_login(request):

    if (request.method == 'POST'):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # First get the username and password supplied
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            # Django's built-in authentication function:
            user = authenticate(username=username, password=password)
            # If we have a user
            if user:
                # Check it the account is active
                if user.is_active:
                    # Log the user in.
                    login(request, user)
                    # Send the user back to homepage
                    return redirect("/")
                else:
                    # If account is not active:
                    return HttpResponse("Your account is not active.")
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(
                    username, password))
                return render(request, 'login.html', {"login_form": LoginForm})
    else:
        # Nothing has been provided for username or password.
        return render(request, 'login.html', {"login_form": LoginForm})


def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return redirect('learner:login')
