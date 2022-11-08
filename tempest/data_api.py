import requests as reqs
import time as tm

def get_date():
     #local time => lt
    lt = tm.localtime(tm.time())
    mon = str(lt.tm_mon)
    day = str(lt.tm_mday)
    if len(mon)<2:
        mon = '0'+mon
    if len(day)<2:
        day = '0'+day
    date = f'{lt.tm_year}{mon}{day}'
    return date

def get_time():
    lt = tm.localtime(tm.time())
    hour = str(lt.tm_hour)
    if len(hour)<2: hour = '0'+hour
    return hour + '00'

def get_past_wthr(date=get_date()):
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
    return res.json()['response']['body']['items']['item'][0]

def get_past_wthr_sum(date=get_date):
    res = get_past_wthr(date)
    result = {
        '관측지점번호': res['stnId'],
        '관측지점이름': res['stnNm'],
        '기상현상': res['iscs'],
        '평균기온': res['avgTa'],
        '최저기온': res['minTa'],
        '최저기온시간': res['minTaHrmt'],
        '최고기온': res['maxTa'],
        '최고기온시간': res['maxTaHrmt'],
        '일강수량': res['sumRn'],
        '평균풍속': res['avgWs'],
        '평균상대습도': res['avgRhm']
    }
    return result



def get_sp_wthr():
    """_summary_
    단기 기상 예보 데이터 호출 
    """
    key='jQGK6Krekt13IVsRLG8PI6pQf+jjzIQjGY2KNi4n6iX9y4Rnl3dd6GVesutZTLvmUNjjy4L6oNmJECojps97JA=='
    url='http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst' # 뒤에 / 붙이지 말 것!!!!!!!!!!!!
    date = get_date()
    base_time = ['0200', '0500', '0800', '1100', '1400', '1700', '2000', '2300'] #(1일 8회)
    params = {
            'serviceKey':  key, # 서비스코드
            'pageNo': '1', # 페이지번호
            'numOfRows':'100', # 한페이지 결과수
            'dataType': 'JSON', # 응답자료형식
            'base_date': date,  # 기반날짜
            'base_time': base_time[1],  # 기반 시간
            'nx': 55, # 예보지점 x좌표, 문자열로 보낼 것!!!
            'ny': 127 # 예보지점 y좌표
            }
    #print(f'debug: params: {params}')
    res = reqs.get(url, params=params, timeout=20)
    #print(f'debug: res: {res}')
    #print(f'\t{res.json()}')
    return res.json()['response']['body']['items']['item']
    