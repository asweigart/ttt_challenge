from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest

from .models import Greeting

import ttt

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')


def ttt_challenge(request):
    try:
        board = ttt.Board(request.GET['board'])
        ai = ttt.TTTAI()
        board.make_move(ttt.O, ai.next_move(board))
    except:
        return HttpResponseBadRequest()

    return HttpResponse(str(board))


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

