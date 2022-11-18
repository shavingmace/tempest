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
from .models import Weather, ClotheRecords, Clothing_outer, Clothing_top, Clothing_bottom, Clothing_etc



# 첫 화면을 브라우저에 렌더링하기 위한 함수
def index(req):
    weather_object = Weather.objects.latest('date')
    weather_json = weather_object.json
    
    # icon 결정
    pty = weather_json['시간별 예보'][get_time()]['PTY']
    sky = weather_json['시간별 예보'][get_time()]['SKY']
    icon =''
    
    #print(f'debug@index {pty}:{type(pty)}, {sky}:{type(sky)}')
    
    # icon 결정 메커니즘 
    if pty=='0': # 강수 상태가 0(안 옴)일 때의 ico 결정 if문
        if sky=='1':icon = '<div class="container_w"><div class="element_w"><svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 44.9 44.9" style="enable-background:new 0 0 44.9 44.9;" xml:space="preserve" height="40px" width="40px"><g id="Sun"><circle id="XMLID_61_" class="yellow_w" cx="22.4" cy="22.6" r="11"/><g><path id="XMLID_60_" class="yellow_w" d="M22.6,8.1h-0.3c-0.3,0-0.6-0.3-0.6-0.6v-7c0-0.3,0.3-0.6,0.6-0.6l0.3,0c0.3,0,0.6,0.3,0.6,0.6 v7C23.2,7.8,22.9,8.1,22.6,8.1z"/><path id="XMLID_59_" class="yellow_w" d="M22.6,36.8h-0.3c-0.3,0-0.6,0.3-0.6,0.6v7c0,0.3,0.3,0.6,0.6,0.6h0.3c0.3,0,0.6-0.3,0.6-0.6v-7 C23.2,37,22.9,36.8,22.6,36.8z"/><path id="XMLID_58_" class="yellow_w" d="M8.1,22.3v0.3c0,0.3-0.3,0.6-0.6,0.6h-7c-0.3,0-0.6-0.3-0.6-0.6l0-0.3c0-0.3,0.3-0.6,0.6-0.6h7 C7.8,21.7,8.1,21.9,8.1,22.3z"/><path id="XMLID_57_" class="yellow_w" d="M36.8,22.3v0.3c0,0.3,0.3,0.6,0.6,0.6h7c0.3,0,0.6-0.3,0.6-0.6v-0.3c0-0.3-0.3-0.6-0.6-0.6h-7 C37,21.7,36.8,21.9,36.8,22.3z"/><path id="XMLID_56_" class="yellow_w" d="M11.4,31.6l0.2,0.3c0.2,0.2,0.2,0.6-0.1,0.8l-5.3,4.5c-0.2,0.2-0.6,0.2-0.8-0.1l-0.2-0.3 c-0.2-0.2-0.2-0.6,0.1-0.8l5.3-4.5C10.9,31.4,11.2,31.4,11.4,31.6z"/><path id="XMLID_55_" class="yellow_w" d="M33.2,13l0.2,0.3c0.2,0.2,0.6,0.3,0.8,0.1l5.3-4.5c0.2-0.2,0.3-0.6,0.1-0.8l-0.2-0.3 c-0.2-0.2-0.6-0.3-0.8-0.1l-5.3,4.5C33,12.4,33,12.7,33.2,13z"/><path id="XMLID_54_" class="yellow_w" d="M11.4,13.2l0.2-0.3c0.2-0.2,0.2-0.6-0.1-0.8L6.3,7.6C6.1,7.4,5.7,7.5,5.5,7.7L5.3,7.9 C5.1,8.2,5.1,8.5,5.4,8.7l5.3,4.5C10.9,13.5,11.2,13.5,11.4,13.2z"/><path id="XMLID_53_" class="yellow_w" d="M33.2,31.9l0.2-0.3c0.2-0.2,0.6-0.3,0.8-0.1l5.3,4.5c0.2,0.2,0.3,0.6,0.1,0.8l-0.2,0.3 c-0.2,0.2-0.6,0.3-0.8,0.1l-5.3-4.5C33,32.5,33,32.1,33.2,31.9z"/><animate attributeType="CSS" attributeName="opacity" attributeType="XML" dur="0.5s" keyTimes="0;0.5;1" repeatCount="indefinite" values="1;0.6;1" calcMode="linear"/></g></g></svg></div></div>'
        # 해 쨍쨍
        if sky=='1':
            if int(get_time()[:2]) < 17:
                icon = '<div class="container_w"><div class="element_w"><svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 44.9 44.9" style="enable-background:new 0 0 44.9 44.9;" xml:space="preserve" height="40px" width="40px"><g id="Sun"><circle id="XMLID_61_" class="yellow_w" cx="22.4" cy="22.6" r="11"/><g><path id="XMLID_60_" class="yellow_w" d="M22.6,8.1h-0.3c-0.3,0-0.6-0.3-0.6-0.6v-7c0-0.3,0.3-0.6,0.6-0.6l0.3,0c0.3,0,0.6,0.3,0.6,0.6 v7C23.2,7.8,22.9,8.1,22.6,8.1z"/><path id="XMLID_59_" class="yellow_w" d="M22.6,36.8h-0.3c-0.3,0-0.6,0.3-0.6,0.6v7c0,0.3,0.3,0.6,0.6,0.6h0.3c0.3,0,0.6-0.3,0.6-0.6v-7 C23.2,37,22.9,36.8,22.6,36.8z"/><path id="XMLID_58_" class="yellow_w" d="M8.1,22.3v0.3c0,0.3-0.3,0.6-0.6,0.6h-7c-0.3,0-0.6-0.3-0.6-0.6l0-0.3c0-0.3,0.3-0.6,0.6-0.6h7 C7.8,21.7,8.1,21.9,8.1,22.3z"/><path id="XMLID_57_" class="yellow_w" d="M36.8,22.3v0.3c0,0.3,0.3,0.6,0.6,0.6h7c0.3,0,0.6-0.3,0.6-0.6v-0.3c0-0.3-0.3-0.6-0.6-0.6h-7 C37,21.7,36.8,21.9,36.8,22.3z"/><path id="XMLID_56_" class="yellow_w" d="M11.4,31.6l0.2,0.3c0.2,0.2,0.2,0.6-0.1,0.8l-5.3,4.5c-0.2,0.2-0.6,0.2-0.8-0.1l-0.2-0.3 c-0.2-0.2-0.2-0.6,0.1-0.8l5.3-4.5C10.9,31.4,11.2,31.4,11.4,31.6z"/><path id="XMLID_55_" class="yellow_w" d="M33.2,13l0.2,0.3c0.2,0.2,0.6,0.3,0.8,0.1l5.3-4.5c0.2-0.2,0.3-0.6,0.1-0.8l-0.2-0.3 c-0.2-0.2-0.6-0.3-0.8-0.1l-5.3,4.5C33,12.4,33,12.7,33.2,13z"/><path id="XMLID_54_" class="yellow_w" d="M11.4,13.2l0.2-0.3c0.2-0.2,0.2-0.6-0.1-0.8L6.3,7.6C6.1,7.4,5.7,7.5,5.5,7.7L5.3,7.9 C5.1,8.2,5.1,8.5,5.4,8.7l5.3,4.5C10.9,13.5,11.2,13.5,11.4,13.2z"/><path id="XMLID_53_" class="yellow_w" d="M33.2,31.9l0.2-0.3c0.2-0.2,0.6-0.3,0.8-0.1l5.3,4.5c0.2,0.2,0.3,0.6,0.1,0.8l-0.2,0.3 c-0.2,0.2-0.6,0.3-0.8,0.1l-5.3-4.5C33,32.5,33,32.1,33.2,31.9z"/><animate attributeType="CSS" attributeName="opacity" attributeType="XML" dur="0.5s" keyTimes="0;0.5;1" repeatCount="indefinite" values="1;0.6;1" calcMode="linear"/></g></g></svg></div></div>'
            else:
                icon = '<div class="container_w"><div class="element_w"><svg version="1.1" id="Layer_1" xmlns="<http://www.w3.org/2000/svg>" xmlns:xlink="<http://www.w3.org/1999/xlink>" x="0px" y="0px" viewBox="0 0 30.8 42.5" style="enable-background:new 0 0 30.8 42.5;" xml:space="preserve" height="40px" width="40px"><path id="Moon" class="yellow_w" d="M15.3,21.4C15,12.1,21.1,4.2,29.7,1.7c-2.8-1.2-5.8-1.8-9.1-1.7C8.9,0.4-0.3,10.1,0,21.9 c0.3,11.7,10.1,20.9,21.9,20.6c3.2-0.1,6.3-0.9,8.9-2.3C22.2,38.3,15.6,30.7,15.3,21.4z"/></svg></div>'
        # 구름
        else: icon = '<div class="container_w"><div class="element_w"><svg version="1.1" id="Layer_1" xmlns="<http://www.w3.org/2000/svg>" xmlns:xlink="<http://www.w3.org/1999/xlink>" x="0px" y="0px" viewBox="0 0 60.7 40" style="enable-background:new 0 0 60.7 40;" xml:space="preserve"><g id="Cloud_1"><g id="White_cloud_1"><path id="XMLID_2_" class="white_w" d="M47.2,40H7.9C3.5,40,0,36.5,0,32.1l0,0c0-4.3,3.5-7.9,7.9-7.9h39.4c4.3,0,7.9,3.5,7.9,7.9v0 C55.1,36.5,51.6,40,47.2,40z"/><circle id="XMLID_3_" class="white_w" cx="17.4" cy="22.8" r="9.3"/><circle id="XMLID_4_" class="white_w" cx="34.5" cy="21.1" r="15.6"/><animateTransform attributeName="transform"attributeType="XML"dur="6s"keyTimes="0;0.5;1"repeatCount="indefinite"type="translate"values="0;5;0"alcMode="linear"></animateTransform></g><g id="Gray_cloud_1"><path id="XMLID_6_" class="gray_w" d="M54.7,22.3H33.4c-3.3,0-6-2.7-6-6v0c0-3.3,2.7-6,6-6h21.3c3.3,0,6,2.7,6,6v0 C60.7,19.6,58,22.3,54.7,22.3z"/><circle id="XMLID_7_" class="gray_w" cx="45.7" cy="10.7" r="10.7"/><animateTransform attributeName="transform"attributeType="XML"dur="6s"keyTimes="0;0.5;1"repeatCount="indefinite"type="translate"values="0;-3;0"calcMode="linear"></animateTransform></g></g></svg></div>'
    # 약한 비
    elif pty=='1': icon = '<div class="container_w"><div class="element_w"><svg version="1.1" id="Layer_1" xmlns="<http://www.w3.org/2000/svg>" xmlns:xlink="<http://www.w3.org/1999/xlink>" x="0px" y="0px" viewBox="0 0 55.1 60" style="enable-background:new 0 0 55.1 49.5;" xml:space="preserve"><g id="Cloud_2"><g id="Rain_2"><path id="rain_2_left" class="white_w" d="M20.7,46.4c0,1.7-1.4,3.1-3.1,3.1s-3.1-1.4-3.1-3.1c0-1.7,3.1-7.8,3.1-7.8 S20.7,44.7,20.7,46.4z"></path><path id="rain_2_mid" class="white_w" d="M31.4,46.4c0,1.7-1.4,3.1-3.1,3.1c-1.7,0-3.1-1.4-3.1-3.1c0-1.7,3.1-7.8,3.1-7.8 S31.4,44.7,31.4,46.4z"></path><path id="rain_2_right" class="white_w" d="M41.3,46.4c0,1.7-1.4,3.1-3.1,3.1c-1.7,0-3.1-1.4-3.1-3.1c0-1.7,3.1-7.8,3.1-7.8 S41.3,44.7,41.3,46.4z"></path><animateTransform attributeName="transform"attributeType="XML"dur="1s"keyTimes="0;1"repeatCount="indefinite"type="translate"values="0 0;0 10"calcMode="linear"></animateTransform><animate attributeType="CSS"attributeName="opacity"attributeType="XML"dur="1s"keyTimes="0;1" repeatCount="indefinite"values="1;0"calcMode="linear"/></g><g id="White_cloud_2"><path id="XMLID_14_" class="white_w" d="M47.2,34.5H7.9c-4.3,0-7.9-3.5-7.9-7.9l0,0c0-4.3,3.5-7.9,7.9-7.9h39.4c4.3,0,7.9,3.5,7.9,7.9 v0C55.1,30.9,51.6,34.5,47.2,34.5z"/><circle id="XMLID_13_" class="white_w" cx="17.4" cy="17.3" r="9.3"/><circle id="XMLID_10_" class="white_w" cx="34.5" cy="15.6" r="15.6"/></g></g></svg></div>'
    # 약한 눈
    elif pty=='2': icon = '<div class="container_w"><div class="element_w"><svg version="1.1" id="Layer_1" xmlns="<http://www.w3.org/2000/svg>" xmlns:xlink="<http://www.w3.org/1999/xlink>" x="0px" y="0px" viewBox="0 0 55.1 52.5" style="enable-background:new 0 0 55.1 52.5;" xml:space="preserve"><g id="Cloud_7"><g id="White_cloud_7"><path id="XMLID_8_" class="white_w" d="M47.2,34.5H7.9c-4.3,0-7.9-3.5-7.9-7.9l0,0c0-4.3,3.5-7.9,7.9-7.9h39.4c4.3,0,7.9,3.5,7.9,7.9 v0C55.1,30.9,51.6,34.5,47.2,34.5z"/><circle id="XMLID_5_" class="white_w" cx="17.4" cy="17.3" r="9.3"/><circle id="XMLID_1_" class="white_w" cx="34.5" cy="15.6" r="15.6"/></g><circle class="white_w" cx="37" cy="43.5" r="3"><animateTransform attributeName="transform"attributeType="XML"dur="1.5s"keyTimes="0;0.33;0.66;1"repeatCount="indefinite"type="translate"values="1 -2;3 2; 1 4; 2 6"calcMode="linear"></animateTransform></circle><circle class="white_w" cx="27" cy="43.5" r="3"><animateTransform attributeName="transform"attributeType="XML" dur="1.5s" keyTimes="0;0.33;0.66;1"repeatCount="indefinite"type="translate"values="1 -2;3 2; 1 4; 2 6"calcMode="linear"></animateTransform></circle><circle class="white_w" cx="17" cy="43.5" r="3"><animateTransform attributeName="transform"attributeType="XML"dur="1.5s"keyTimes="0;0.33;0.66;1"repeatCount="indefinite"type="translate"values="1 -2;3 2; 1 4; 2 6"calcMode="linear"></animateTransform></circle></g></svg></div></div>'
    # 눈폭풍
    elif pty=='3': icon = '<div class="container_w"><div class="element_w"><svg version="1.1" id="Layer_1" xmlns="<http://www.w3.org/2000/svg>" xmlns:xlink="<http://www.w3.org/1999/xlink>" x="0px" y="0px" viewBox="0 0 55.1 52.5" style="enable-background:new 0 0 55.1 52.5;" xml:space="preserve"><g id="Cloud_7"><g id="White_cloud_7"><path id="XMLID_8_" class="white_w" d="M47.2,34.5H7.9c-4.3,0-7.9-3.5-7.9-7.9l0,0c0-4.3,3.5-7.9,7.9-7.9h39.4c4.3,0,7.9,3.5,7.9,7.9 v0C55.1,30.9,51.6,34.5,47.2,34.5z"/><circle id="XMLID_5_" class="white_w" cx="17.4" cy="17.3" r="9.3"/><circle id="XMLID_1_" class="white_w" cx="34.5" cy="15.6" r="15.6"/></g><circle class="white_w" cx="37" cy="43.5" r="3"><animateTransform attributeName="transform"attributeType="XML"dur="1.5s"keyTimes="0;0.33;0.66;1"repeatCount="indefinite"type="translate"values="1 -2;3 2; 1 4; 2 6"calcMode="linear"></animateTransform></circle><circle class="white_w" cx="27" cy="43.5" r="3"><animateTransform attributeName="transform"attributeType="XML" dur="1.5s" keyTimes="0;0.33;0.66;1"repeatCount="indefinite"type="translate"values="1 -2;3 2; 1 4; 2 6"calcMode="linear"></animateTransform></circle><circle class="white_w" cx="17" cy="43.5" r="3"><animateTransform attributeName="transform"attributeType="XML"dur="1.5s"keyTimes="0;0.33;0.66;1"repeatCount="indefinite"type="translate"values="1 -2;3 2; 1 4; 2 6"calcMode="linear"></animateTransform></circle></g></svg></div></div>'
    # 폭풍우
    elif pty=='4': icon = '<div class="container_w"><div class="element_w"><svg version="1.1" id="Layer_1" xmlns="<http://www.w3.org/2000/svg>" xmlns:xlink="<http://www.w3.org/1999/xlink>" x="0px" y="0px" viewBox="0 0 60.7 80" style="enable-background:new 0 0 60.7 55;" xml:space="preserve"><g id="Cloud_6"><g id="White_cloud_6"><path id="XMLID_81_" class="white_w" d="M47.2,40H7.9C3.5,40,0,36.5,0,32.1l0,0c0-4.3,3.5-7.9,7.9-7.9h39.4c4.3,0,7.9,3.5,7.9,7.9v0 C55.1,36.5,51.6,40,47.2,40z"/><circle id="XMLID_80_" class="white_w" cx="17.4" cy="22.8" r="9.3"/><circle id="XMLID_77_" class="white_w" cx="34.5" cy="21.1" r="15.6"/></g><g id="Gray_cloud_6"><path id="XMLID_75_" class="gray_w" d="M54.7,22.3H33.4c-3.3,0-6-2.7-6-6v0c0-3.3,2.7-6,6-6h21.3c3.3,0,6,2.7,6,6v0 C60.7,19.6,58,22.3,54.7,22.3z"/><circle id="XMLID_74_" class="gray_w" cx="45.7" cy="10.7" r="10.7"/><animateTransform attributeName="transform"attributeType="XML"dur="6s"keyTimes="0;0.5;1"repeatCount="indefinite"type="translate"values="0;-3;0"calcMode="linear"></animateTransform></g><g id="Lightning_6"><path id="XMLID_94_" class="yellow_w" d="M43.6,22.7c-0.2,0.6-0.4,1.3-0.6,1.9c-0.2,0.6-0.4,1.2-0.7,1.8c-0.4,1.2-0.9,2.4-1.5,3.5c-1,2.3-2.2,4.6-3.4,6.8l-1.7-2.9c3.2-0.1,6.3-0.1,9.5,0l3,0.1l-1.3,2.5c-1.1,2.1-2.2,4.2-3.5,6.2c-0.6,1-1.3,2-2,3c-0.7,1-1.4,2-2.2,2.9c0.2-1.2,0.5-2.4,0.8-3.5c0.3-1.2,0.6-2.3,1-3.4c0.7-2.3,1.5-4.5,2.4-6.7l1.7,2.7c-3.2,0.1-6.3,0.2-9.5,0l-3.4-0.1l1.8-2.8c1.4-2.1,2.8-4.2,4.3-6.2c0.8-1,1.6-2,2.4-3c0.4-0.5,0.8-1,1.3-1.5C42.7,23.7,43.1,23.2,43.6,22.7z"/><animate attributeType="CSS"attributeName="opacity"attributeType="XML"dur="1.5s"keyTimes="0;0.5;1"repeatCount="indefinite"values="1;0;1"calcMode="linear"/></g><g id="Rain_6"><path id="Rain_6_right" class="white_w" d="M36.3,51.9c0,1.7-1.4,3.1-3.1,3.1c-1.7,0-3.1-1.4-3.1-3.1c0-1.7,3.1-7.8,3.1-7.8 S36.3,50.2,36.3,51.9z"/><path id="Rain_6_mid" class="white_w" d="M26.4,51.9c0,1.7-1.4,3.1-3.1,3.1c-1.7,0-3.1-1.4-3.1-3.1c0-1.7,3.1-7.8,3.1-7.8 S26.4,50.2,26.4,51.9z"/><path id="Rain_6_left" class="white_w" d="M15.7,51.9c0,1.7-1.4,3.1-3.1,3.1s-3.1-1.4-3.1-3.1c0-1.7,3.1-7.8,3.1-7.8 S15.7,50.2,15.7,51.9z"/><animateTransform attributeName="transform"attributeType="XML"dur="1s"keyTimes="0;1"repeatCount="indefinite"type="translate"values="0 0;0 10"calcMode="linear"></animateTransform><animate attributeType="CSS"attributeName="opacity"attributeType="XML"dur="1s"keyTimes="0;1"repeatCount="indefinite"values="1;0"calcMode="linear"/></g></g></svg></div>'
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
    outer_db =  Clothing_outer.objects.filter()
    top_db = Clothing_top.objects.filter()
    bottom_db = Clothing_bottom.objects.filter()
    etc_db = Clothing_etc.objects.filter()
    
    outer_ls = {} 
    top_ls = {} 
    bottom_ls = {} 
    etc_ls = {} 
    
    for elem in outer_db:
        outer_ls.update({elem.name: { 'name': elem.name, 
                                    'img_path': elem.img_path}})
    for elem in top_db:
        top_ls.update({elem.name: { 'name': elem.name, 
                                    'img_path': elem.img_path}})
    for elem in bottom_db:
        bottom_ls.update({elem.name: { 'name': elem.name, 
                                    'img_path': elem.img_path}})
    for elem in etc_db:
        etc_ls.update({elem.name: { 'name': elem.name, 
                                    'img_path': elem.img_path}})    
    
        
    context = {'outer': outer_ls,
               'top': top_ls,
               'bottom': bottom_ls,
               'etc': etc_ls,
               }

    #print(f'debug@record_form {context}')
    return render(req, 'pagetwo.html', context)


# json 형식으로 옷 기록을 처리하는 view 함수
@login_required(login_url='common:login') 
def record_post(req):
    user = get_object_or_404(TempestUser, pk=req.user.id)
    #print(f'debug: 사용자: {user}')
    form = RecordForm()
    if req.method == 'POST':
        # 먼저 상의와 하의 정보가 들어왔는지 체크
        #print(f'debug@record_post: \n\t req.POST.keys(): \n\t\t {req.POST.keys()}')

        top_check = False
        bottom_check = False

        for key in req.POST.keys():
            if 'top' in key: top_check = True
            elif 'bottom' in key: bottom_check = True
        #print(f'debug==1 {str(top_check)}')
        #print(f'debug==2 {str(bottom_check)}')
        #print('debug==', str((top_check is True) and (bottom_check is True)))
        if (top_check and bottom_check):
            #print(f'debug@record_post - checked: {top_check}, {bottom_check}')
            pass
        else:
            #print(f'debug@record_post - entered else')
            context = {
                "outer": [x.name for x in Clothing_outer.objects.filter()],
                "top": [x.name for x in Clothing_top.objects.filter()],
                "bottom":[x.name for x in Clothing_bottom.objects.filter()],
                "etc":[x.name for x in Clothing_etc.objects.filter()],
                'error': {
                    'top': not top_check,
                    'bottom': not bottom_check
                }
            }
            #print(f'debug@record_post - context: \n {context["error"]}')
            return render(req, 'pagetwo.html', context)
        
        # 체크 했으면 필요한 정보만 담는다. 
        clothes_data = {
            'outer':[],
            'top':[],
            'bottom':[],
            'etc':[]
            }
        
        for key in req.POST.keys():
            if 'outer' in key:
                clothes_data['outer'].append(req.POST[key])
            elif 'top' in key:
                clothes_data['top'].append(req.POST[key])
            if 'bottom' in key:
                clothes_data['bottom'].append(req.POST[key])
            if 'etc' in key:
                clothes_data['etc'].append(req.POST[key])
        
        record = form.save(commit=False)
        record.user = user
        record.weather = Weather.objects.latest('date')
        record.clothes = clothes_data
        #print(f'debug: @record_post \n\trecord = {record}')
        record.save()
        return redirect('tempest:recorded') # 기록 작성 후 리디렉션
    else:
        # form = AnswerForm() # 이 경우도 GET 메서드로 요청됨, 그러나 content 필드가 not None이라는 조건이 있으므로 처리되지 않음. 
        #print(f'debug: requested without POST')
        return HttpResponseNotAllowed("POST 방식의 요청만 가능합니다.") # 명시적으로 POST 방식 이외의 처리를 거부함. 



# 3번째 화면을 보여주는 view 함수 
@login_required(login_url='common:login') 
def recorded(req):
    filterlist = ClotheRecords.objects.filter(user=req.user).order_by('-id')
    record = filterlist.latest('id') # 사용자의 기록 호출
    #print(f'debug@recorded - record는 {record}')
    
    
    outer_ls =  Clothing_outer.objects.filter()
    top_ls = Clothing_top.objects.filter()
    bottom_ls = Clothing_bottom.objects.filter()
    etc_ls = Clothing_etc.objects.filter()
    
    outer_records = {} 
    top_records = {} 
    bottom_records = {} 
    etc_records = {} 
    
    for category, user_clothings in record.clothes.items():
        #print(f'debug: {category}: {user_clothings}')
        
        for elem in user_clothings:
            for outer in outer_ls:
                if elem == outer.name:
                    outer_records.update({elem: { 'name': elem,
                                            'cat': '아우터', 
                                           'img_path': outer.img_path}})
            for top in top_ls:
                if elem == top.name:
                    top_records.update({elem: {'name': elem,
                                           'cat': '상의', 
                                           'img_path': top.img_path}})
            for bottom in bottom_ls:
                if elem == bottom.name:
                    bottom_records.update({elem: {'name': elem,
                                           'cat': '하의', 
                                           'img_path': bottom.img_path} })
            for etc in etc_ls:
                if elem == etc.name:
                    etc_records.update({elem: {'name': elem,
                                           'cat': '액세서리', 
                                           'img_path': etc.img_path}})

    context = {'outer_records': outer_records,
               'top_records': top_records,
               'bottom_records': bottom_records,
               'etc_records': etc_records,
               }
    #print(f'debug: @recorded - five records: {context}')
    
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



