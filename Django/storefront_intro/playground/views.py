from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# request -> response (action in other frameworks, Django calls it view)


def say_Hello(request):
    return render(request, "hello.html", {"name": "Daniel"})
