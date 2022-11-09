from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .data_api import *
from .models import Weather
from django.utils import timezone

# Create your views here.

def test(req):
    return HttpResponse("Tempest 시험 가동")

def index(req):
    weather_object = Weather.objects.latest('date')
    weather_json = weather_object.json
    #print('debug!!', weather_json)
    context = {'date': timezone.now(),  
               'tmx': weather_json['TMX'],
               'tmn': weather_json['TMN'],
               'last_update_time': f'{str(weather_object.baseDate)}-{str(weather_object.baseTime)}' 
            }
    print(f'debg: {context}')
    return render(req, 'tempest/index.html', context)

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


def record_current_wthr(req):
    record_sp_wthr()
    res_json={}
    try:
        res_json = get_sp_wthr_sum()
    except Exception as e:
        print(f'\t오류: {e}')
        
    return JsonResponse(res_json, safe=False, json_dumps_params={'ensure_ascii': False})


def show_past_wthr(req, date=get_date()):
    try:
        # res_json = get_wthr(date)
        res_json = get_past_wthr_sum(date)
        print(f'\tdebug: 평균기온: {res_json["평균기온"]}')
    except Exception as e:
        print(f'\tdebug: @show_wthr에서 Error 발생:\n\t {e}')
        res_json = {"msg": '오류가 있습니다.'}
    print(get_date())
    
    return JsonResponse(res_json, safe=False, json_dumps_params={'ensure_ascii': False})