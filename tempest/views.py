from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def test(req):
    return HttpResponse("Tempest 시험 가동")

def index(req):
    return HttpResponse("안녕 템페스트")