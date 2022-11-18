import requests as reqs
import time as tm
from datetime import date, timedelta
from .models import Weather
from django.utils import timezone

# 기상청 API에서 데이터를 수집하기 위한 함수들 

def get_date():
    """_summary_
        현재 날짜를 가져오는 함수.

    Returns:
        문자열로 포맷한 오늘 날짜를 반환함
    """
    today = date.today() 
    return today.strftime('%Y%m%d')

def get_past():
    """_summary_
        어제 날짜를 가져오는 함수.
    """
    yesterday = date.today() - timedelta(1)
    return yesterday.strftime('%Y%m%d')

def get_time():
    """_summary_
        현재 시간을 가져오는 함수.
    
    Returns:
        반환하는 시간은 0900, 1300 등 형식이어야 함.
    """
    lt = tm.localtime(tm.time())
    hour = str(lt.tm_hour)
    # 현재 시간이 한 자릿 수, 즉 10시 이전 1~9시 이면 앞에 0을 붙임
    if len(hour)<2: hour = '0'+hour
    #  
    # 형식을 맞추기 위해 뒤에 00을 붙여준다. 분은 0으로 통일.
    return hour + '00'


def get_past_wthr(date=get_date()):
    """_summary_
        API가 제공하는 데이터를 지저분하게 받아오기만 하는 함수
        개발 중 만들었고 아래 함수에서 다시 사용함.  
        지금은 자세히 분석하지 않기를 권고함.
    """
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



def get_past_wthr_sum(date=get_date()): #기본 입력으로 오늘 날짜를 가져오게 함. 
    """_summary_
        단기 예보가 아니라 현재까지 축적된 여러 기상 정보를 가져오는 함수. 
        아주 오래 전부터 하루 전까지의 기상정보를 불러올 수 있음.
    
    Args:
        date: 원하는 날짜의 데이터 

    Returns:
        json: 기상 데이터 반환
    """
    # 위에서 만든 함수를 사용해 res에 데이터를 담음. 
    res = get_past_wthr(date)
    # 원시적 json에서 우리에게 필요한 데이터만 빼냄. 
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

# get short period weather의 단축어. 
def get_sp_wthr(bt_unit=1, date=get_date(), gps_loc=(55, 127)):
    """_summary_
        단기 기상 예보 데이터 호출 
    """
    key='jQGK6Krekt13IVsRLG8PI6pQf+jjzIQjGY2KNi4n6iX9y4Rnl3dd6GVesutZTLvmUNjjy4L6oNmJECojps97JA=='
    url='http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst' # 뒤에 / 붙이지 말 것!!!!!!!!!!!!
    
    # 단기 기상 예보의 데이터 제공 시간은 법정 기준으로 정해져있다. 
    base_time = ['0200', '0500', '0800', '1100', '1400', '1700', '2000', '2300'] #(1일 8회)
    # 함수 인자인 bt_unit은 위 8개 법정 시간 중 하나를 택할 때 사용한다. 기본 값은 인덱스 1, 즉 0500 이다. 
    
    params = {
            'serviceKey':  key, # 서비스코드
            'pageNo': '1', # 페이지번호
            'numOfRows':'3000', # 한페이지 결과수
            'dataType': 'JSON', # 응답자료형식
            'base_date': date,  # 기반날짜
            'base_time': base_time[bt_unit],  # 기반 시간
            'nx': gps_loc[0], # 예보지점 x좌표
            'ny': gps_loc[1] # 예보지점 y좌표
            }
    #print(f'debug: params: {params}')
    
    res = reqs.get(url, params=params, timeout=30) # timeout은 응답을 기다리는 시간. 넉넉히 30초 줬다.
    #print(f'debug: res: {res}')
    #print(f'\t{res.json()}')
    
    # 데이터를 보기 전엔 직관적으론 이해가 안 되겠지만 
    # api에서 받는 원시 json에서 필요한 정보가 저 즈음 인덱스에 들어있다. 
    return res.json()['response']['body']['items']['item']


def get_sp_wthr_sum():
    """_summary_
        위 함수에서 필요한 정보만 가져오도록 한 것. 
        get short period weather summary의 단축어. 한글로는 '단기 기상 예보 요약'이다. 
        **크론에 이 함수를 추가해 법정 시간에 작동하도록 예약해두었기 때문에 
        크론에 예약되지 않은 시간에 불러왔을 때의 작동 방식이 정의되어 있다.**
    Returns:
        _type_: _description_
    """
    base_time = ['0200', '0500', '0800', '1100', 
                 '1400', '1700', '2000', '2300'] #(1일 8회)
    
    btime = get_time()
    date = get_date()
    yesterday = get_past()
    
    result = {date:{ btime:{ } } } #결과를 담을 딕셔너리 자료형
    print(f'debug$ \n    함수호출시간: {get_time()}') 
    
    try:
        if btime in base_time: # 현재 시간이 base_time에 포함되어 있는지 확인한다. 포함되어 있다면 그냥 작동한다. 
            res = get_sp_wthr(base_time.index(btime))
            print(f'기준발표 시간: {btime}\n')
        else: # 크론에 예약되지 않은 시간에 작동할 때, 예컨대 관리자가 임의로 날씨를 기록할 때 작동한다. 
            print('#==크론 예약 외 시간==#')
            res = get_sp_wthr()
        res_past = get_sp_wthr(7, yesterday) # 단기 예보에서는 어제 날씨 응답이 필요하다. 최저 기온은 전날 예보하기 때문. 
    except Exception as e:
        print(f'오류: {e}')
        pass
    #print(f'debug$ res: {res[:3]}')
    #print(f'debug$ res_past: {res_past[:3]}')
    
    # 오늘 날씨 응답과 어제 날씨 응답 결과를 합친다 
    res.extend(res_past) # 리스트 연결용 메서드 extend()
    #print(f'debug$ res extended: {res[:3]}\n')
    
    # 예보 시간별로 데이터를 저장하기 위해 딕셔너리를 만든다.
    result[date][btime]['시간별 예보']= {}  
    
    # 집합 자료형으로 예보 시간이 중복되지 않게 결과 딕셔너리에 추가한다. 
    fcstTime_ls = []
    for elem in res: 
        fcstTime_ls.append(elem['fcstTime'])
    
    fcstTime_set = set(fcstTime_ls) 
    #print(f'debug$ fcstTime_set: {fcstTime_set}')
    for fcstTime in fcstTime_set:
        result[date][btime]['시간별 예보'].update({fcstTime: {}})
    
    for elem in res:
        # 우리에게 필요한 데이터 코드 카테고리는 
            # SKY, PTY, TMN, TMX 
            # 각각 하늘 상태, 강수 형태, 최저기온, 최고기온
        
        # 먼저 하늘 상태, 강수 형태, 현재 기온을 따로 빼서 저장한다. 
        if elem['category'] in ['SKY', 'PTY', 'TMP'] and elem['fcstDate']==date:
            #print('debug:', elem)

            # 반환용 결과 딕셔너리의 result[date][btime]['시간별 예보']에 
                # 예보시간을 인덱스로 추가하고 >> elem['fcstTime']
                # 위 카테고리에 포함된 기상예보 정보를 예보시간(elem['fcstValue'])과 함께 추가한다. 
            result[date][btime]['시간별 예보'][elem['fcstTime']].update({elem['category']:elem['fcstValue'] })
            
        # 최고기온, 최저기온을 따로 보관해둔다. 
        elif elem['category'] in ['TMN', "TMX"] and elem['fcstDate']==date:
            # 위 if 문과 비슷한 방식으로 작동한다. 
            result[date][btime].update({elem['category']:elem['fcstValue'] })
    print(f'debug$ result: {result}\n----')
    
    return result # json 형식으로 결과 반환.


def record_sp_wthr():
    json = get_sp_wthr_sum()
    weather = Weather()
    weather.date = timezone.now()
    weather.baseDate = get_date()
    weather.region = '서울'
    weather.baseTime = get_time()
    temp = json[list(json.keys())[0]]
    weather.json = temp[list(temp.keys())[0]]
    weather.save()
    print(f'날씨 업데이트: \n\t시간:{weather.baseTime}\n\tWeather 객체:{weather}')
    return
