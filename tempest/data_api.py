import requests as reqs

def get_wthr(date):
    key='jQGK6Krekt13IVsRLG8PI6pQf+jjzIQjGY2KNi4n6iX9y4Rnl3dd6GVesutZTLvmUNjjy4L6oNmJECojps97JA=='
    url='http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'
    params = {
            'serviceKey':  key, # 서비스코드
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
    return res.json()