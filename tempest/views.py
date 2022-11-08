from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .data_api import get_wthr

# Create your views here.

def test(req):
    return HttpResponse("Tempest 시험 가동")

def index(req):
    return HttpResponse("안녕 템페스트")

def jsontest(req):
    j = {
         '쥐': {
            '함성': '우하하',
            "음식": '치즈',
            '집': '땅굴'
            },
         '소':{
            '함성': '음하하',
            '음식':'치즈양파수프',
            '집':'외양간'
         }
         }
    print(f"json test 시작")
    return JsonResponse(j, safe=False, json_dumps_params={'ensure_ascii': False})


def show_wthr(req, date):
    try:
        res_json = get_wthr(date)
    except Exception as e:
        print(f'@show_wthr에서 Error 발생:\n\t {e}')
        res_json = {"msg": '오류가 있습니다.'}
    
    return JsonResponse(res_json, safe=False, json_dumps_params={'ensure_ascii': False})
