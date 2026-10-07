from django.http import HttpResponse


def index(request):
    return HttpResponse("communication is wired up.")
