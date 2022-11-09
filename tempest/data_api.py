import requests as reqs
import time as tm
from datetime import date, timedelta
 

def get_date():
    today = date.today()
    return today.strftime('%Y%m%d')

def get_past():
    yesterday = date.today() - timedelta(1)
    return yesterday.strftime('%Y%m%d')

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


# get short period weather
def get_sp_wthr(bt_unit=1, date=get_date()):
    """_summary_
    단기 기상 예보 데이터 호출 
    """
    key='jQGK6Krekt13IVsRLG8PI6pQf+jjzIQjGY2KNi4n6iX9y4Rnl3dd6GVesutZTLvmUNjjy4L6oNmJECojps97JA=='
    url='http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst' # 뒤에 / 붙이지 말 것!!!!!!!!!!!!
    base_time = ['0200', '0500', '0800', '1100', '1400', '1700', '2000', '2300'] #(1일 8회)
    params = {
            'serviceKey':  key, # 서비스코드
            'pageNo': '1', # 페이지번호
            'numOfRows':'3000', # 한페이지 결과수
            'dataType': 'JSON', # 응답자료형식
            'base_date': date,  # 기반날짜
            'base_time': base_time[bt_unit],  # 기반 시간
            'nx': 55, # 예보지점 x좌표, 문자열로 보낼 것!!!
            'ny': 127 # 예보지점 y좌표
            }
    #print(f'debug: params: {params}')
    res = reqs.get(url, params=params, timeout=20)
    #print(f'debug: res: {res}')
    #print(f'\t{res.json()}')
    return res.json()['response']['body']['items']['item']

def get_sp_wthr_sum(bt_unit):
    base_time = ['0200', '0500', '0800', '1100', '1400', '1700', '2000', '2300'] #(1일 8회)
    btime = base_time[bt_unit]
    date = get_date()
    yesterday = get_past()
    result = {date:{ btime:{ } } } #결과를 담을 딕셔너리 자료형
    print(f'debug$ \n    함수호출시간: {get_time()}, \n    기준발표 시간: {btime}\n')
    
    res = get_sp_wthr(bt_unit)
    res_past = get_sp_wthr(7, yesterday) # 어제 날씨 응답이 필요하다. 최저 기온은 전날 예보하기 때문. 
    #print(f'debug$ res: {res[:3]}')
    #print(f'debug$ res_past: {res_past[:3]}')
    
    # 오늘 날씨 응답과 어제 날씨 응답 결과를 합친다 
    res.extend(res_past)
    print(f'debug$ res extended: {res[:3]}\n')
    
    fcstTime_ls = []
    for elem in res: 
        fcstTime_ls.append(elem['fcstTime'])
    
    result[date][btime]['시간별 예보']= {}
    fcstTime_set = set(fcstTime_ls) # 집합 자료형으로 예보 시간이 중복되지 않게 결과 딕셔너리에 추가한다. 
    #print(f'debug$ fcstTime_set: {fcstTime_set}')
    for fcstTime in fcstTime_set:
        result[date][btime]['시간별 예보'].update({fcstTime: {}})
        
    for elem in res:
        # 우리에게 필요한 데이터 코드 SKY, PTY, TMN, TMX; 각각 하늘 상태, 강수 형태, 최저기온, 최고기온
        if elem['category'] in ['SKY', 'PTY'] and elem['fcstDate']==date:
            #print('debug:', elem)
            result[date][btime]['시간별 예보'][elem['fcstTime']].update({elem['category']:elem['fcstValue'] })
        elif elem['category'] in ['TMN', "TMX"] and elem['fcstDate']==date:
            result[date][btime].update({elem['category']:elem['fcstValue'] })
    print(f'debug$ result: {result}\n----')
    return result