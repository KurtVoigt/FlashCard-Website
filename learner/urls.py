from django.urls import path

from . import views

app_name = "learner"
urlpatterns = [
    path('', views.index, name='index'),
	path('join', views.join, name= "join"),
    path('login', views.user_login, name = "login"),
    path('logout', views.user_logout, name = "logout"),
    path('dashboard', views.dash, name = "dashboard"),
    path('deck/add', views.deck_add, name='deckAdd'),
    path('card/add/<int:deckId>', views.card_add, name = "cardAdd"),
    path('deck/<int:deckId>', views.deck_review, name='deckReview'),
    path('deck/<int:deckId>/answer', views.card_answer, name='answer'),
    path('deck/<int:deckId>/delete', views.deck_delete, name = 'deckDelete'),
]
