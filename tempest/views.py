from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

import json
import requests as reqs

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
    key='jQGK6Krekt13IVsRLG8PI6pQf+jjzIQjGY2KNi4n6iX9y4Rnl3dd6GVesutZTLvmUNjjy4L6oNmJECojps97JA=='
    url='http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'
    params = {
            'serviceKey':  key,    # 서비스코드
            'pageNo': '1', # 페이지번호
            'numOfRows':'10', # 한페이지 결과수
            'dataType': 'JSON', # 응답자료형식
            'dataCd': 'ASOS',  # 자료코드
            'dateCd': 'DAY',  # 날짜코드
            'startDt': date,  # 조회 기간 시작일(YYYYMMDD)
            'endDt': date,  # 조회 기간 종료일(YYYYMMDD) (전일(D-1)까지 제공)
            'stnIds': '108'  # 종관기상관측 지점 번호 (108 서울)
            }
    res = reqs.get(url, params=params, timeout=10)
    return JsonResponse(res.json(), safe=False, json_dumps_params={'ensure_ascii': False})
