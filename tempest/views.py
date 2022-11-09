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
    
    #icon 결정
    pty = weather_json['시간별 예보'][get_time()]['PTY']
    sky = weather_json['시간별 예보'][get_time()]['SKY']
    icon =''
    
    print(f'debug {pty}:{type(pty)}, {sky}:{type(sky)}')
    
    if pty=='0':
        if sky=='1':icon = 'fas fa-sun'
        else: icon = 'fas fa-smog'
    elif pty=='1': icon = 'fas fa-cloud-showers-heavy'
    elif pty=='2': icon = 'fas fa-cloud-meatball'
    elif pty=='3': icon = 'fas fa-snowflake'
    elif pty=='4': icon = 'fas fa-poo-storm'
    else: icon = 'error'
    
    
    context = {'date': timezone.now(),  
               'tmx': weather_json['TMX'],
               'tmn': weather_json['TMN'],
               'tmp': weather_json['시간별 예보'][get_time()]['TMP'],
               'last_update_time': f'{weather_object.baseDate}-{weather_object.baseTime}',
               'icon': icon
            }

    return render(req, 'tempest/index.html', context)


def second(req):
    from .forms import RecordForm 
    form = RecordForm()
    
    context={'form': form}
    return render(req, 'pagetwo.html', context)


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