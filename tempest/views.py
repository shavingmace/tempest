from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse


# Create your views here.

def test(req):
    return HttpResponse("Tempest 시험 가동")

def index(req):
    return HttpResponse("안녕 템페스트")

def jsontest(req):
    j = {'함성': '우하하',
         '동물': '쥐',
         "음식": '치즈'}
    print(f"json test 시작")
    return JsonResponse(j, safe=False, json_dumps_params={'ensure_ascii': False})