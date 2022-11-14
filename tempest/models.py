from django.db import models
from common.models import TempestUser
import jsonfield  # json 데이터를 데이터베이스에 저장하기 위한 라이브러리


# 사용자는 common.models.py에 정의됨.
    
# 날씨
class Weather(models.Model):
    # 날짜, 지역, API 응답
    date = models.DateTimeField()
    region =  models.CharField(max_length=10)
    baseDate = models.CharField(max_length=10)
    baseTime = models.CharField(max_length=10)
    json = jsonfield.JSONField()

    def __str__(self):
        return f'{self.id}: \n\t{self.date}\n\t{self.region}\n\t{self.baseTime}'

# 피복 범주별 테이블 
# top, outer, bottom, onepiece, shoes, headwear
class Clothing_top(models.Model):
    name = models.CharField(max_length=10)
    def __str__(self): return self.name
    
class Clothing_outer(models.Model):
    name = models.CharField(max_length=10)
    def __str__(self): return self.name

class Clothing_bottom(models.Model):
    name = models.CharField(max_length=10)
    def __str__(self): return self.name
    
class Clothing_etc(models.Model):
    name = models.CharField(max_length=10)
    def __str__(self): return self.name
        
        
# 피복 기록 
class ClotheRecords(models.Model):
    user = models.ForeignKey(TempestUser, on_delete=models.CASCADE)
    weather = models.ForeignKey(Weather, on_delete=models.CASCADE)
    top = models.ForeignKey(Clothing_top, on_delete=models.CASCADE)
    outer = models.ForeignKey(Clothing_outer, on_delete=models.CASCADE)
    bottom =models.ForeignKey(Clothing_bottom, on_delete=models.CASCADE)
    etc = models.ForeignKey(Clothing_etc, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user.username}\n{self.weather.date}\n\touter:{self.outer}\n\ttop:{self.top}\n\tbottom:{self.bottom}'