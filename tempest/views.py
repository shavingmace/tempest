from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from django.http import JsonResponse
from .data_api import *
from .models import Weather, ClotheRecords
from .forms import RecordForm
from common.models import TempestUser
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.conf import settings


# 첫 화면을 브라우저에 렌더링하기 위한 함수
def index(req):
    weather_object = Weather.objects.latest('date')
    weather_json = weather_object.json
    
    # icon 결정
    pty = weather_json['시간별 예보'][get_time()]['PTY']
    sky = weather_json['시간별 예보'][get_time()]['SKY']
    icon =''
    
    print(f'debug {pty}:{type(pty)}, {sky}:{type(sky)}')
    
    # icon 결정 메커니즘 
    if pty=='0': # 강수 상태가 0(안 옴)일 때의 ico 결정 if문
        if sky=='1':icon = 'fas fa-sun'
        else: icon = 'fas fa-smog'
    elif pty=='1': icon = 'fas fa-cloud-showers-heavy'
    elif pty=='2': icon = 'fas fa-cloud-meatball'
    elif pty=='3': icon = 'fas fa-snowflake'
    elif pty=='4': icon = 'fas fa-poo-storm'
    else: icon = 'error'
    
    
    context = {'date': timezone.now(),   #현재 날짜 
               'tmx': weather_json['TMX'], #최고기온
               'tmn': weather_json['TMN'], #최저기온 
               'tmp': weather_json['시간별 예보'][get_time()]['TMP'], # 현재온도 
               'last_update_time': f'{weather_object.baseDate}-{weather_object.baseTime}', # 현재 표시되는 날씨 데이터의 기준 시간
               'icon': icon
            }

    return render(req, 'tempest/index.html', context)

# 두 번째 화면(옷 기록 남기기)을 출력하기 위한 view 함수
# @login_rquired는 로그인 하지 않으면 해당 view 함수를 사용할 수 없게 하는 데코레이터
    # 로그인을 하지 않으면 로그인 URL로 강제 리디렉션 한다. 
    # 여기서 로그인 URL 함수는 common의 view의 login()
@login_required(login_url='common:login') 
def record_form(req):
    from .forms import RecordForm
    form = RecordForm()
    context={
        'form': form
        }
    return render(req, 'pagetwo.html', context)

@login_required(login_url='common:login') 
def record_post(req):
    user = get_object_or_404(TempestUser, pk=req.user.id)
    print(f'debug: 사용자: {user}')
    if req.method == 'POST':
        form = RecordForm(req.POST)
        #print(form)
        if form.is_valid():
            record = form.save(commit=False)
            #print(record)
            record.user = user
            record.weather = Weather.objects.latest('date')
            print(record)
            record.save()
            return redirect('tempest:recorded',  qid=record.id) # 기록 작성 후 리디렉션
    else:
        # form = AnswerForm() # 이 경우도 GET 메서드로 요청됨, 그러나 content 필드가 not None이라는 조건이 있으므로 처리되지 않음. 
        print(f'debug: form failed!!!!')
        return HttpResponseNotAllowed("POST 방식의 요청만 가능합니다.") # 명시적으로 POST 방식 이외의 처리를 거부함. 
    context = {'record':record}
    return render(req, 'pagetwo.html', context)


# 3번째 화면에서 나옴 
@login_required(login_url='common:login') 
def recorded(req):
    record = ClotheRecords.objects.filter(user=req.user).first()
    context = {'record': record}
    return render(req, 'tempest/recorded.html', context)



# 개발 및 운영 중 유용한 함수.
# 현재 단기 예보를 (크론에 예약되지 않은 시점에도) 바로 불러오고 데이터베이스에 기록함.
# 외래키로 쓸 날씨가 없을 때 등 상황에 사용 가능. 
def record_current_wthr(req):
    record_sp_wthr()
    res_json={}
    try:
        res_json = get_sp_wthr_sum()
    except Exception as e:
        print(f'\t오류: {e}')
        
    return JsonResponse(res_json, safe=False, json_dumps_params={'ensure_ascii': False})



# 밑으로는 개발 실험용으로 현재 시점에서는 별로 중요한 함수가 아닙니다. 

# 테스트용 함수. 
# 제일 처음에 화면이 잘 출력되는가를 시험하기 위해 사용했음. 
def test(req):
    return HttpResponse("Tempest 시험 가동")

# json 형식 데이터를 브라우저에 출력하는 것을 시험함. 
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

# 현재 단기 예보를 못생긴 json 날 것 그대로 브라우저에 출력함. 
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



