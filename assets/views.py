from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("Lab Assets Management.")


def import_from_csv(request, module):
    return HttpResponse("Import Data from CSV file.")