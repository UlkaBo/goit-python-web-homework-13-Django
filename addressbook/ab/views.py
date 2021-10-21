from django.http import HttpResponse
#from django.shortcuts import render
from django.template import loader
from .models import Abonent, Phone


def index(request):
    all_abonent = Abonent.objects.all()
    template = loader.get_template("ab/index.html")
    context = {
        'result': all_abonent
    }
    return HttpResponse(template.render(context, request))


def one_person(request, abonent_id):
    return HttpResponse(f'here is one person {abonent_id}')
