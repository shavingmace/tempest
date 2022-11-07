from django.db import models

# 만들어야 할 모델 
# 사용자, 날씨, 의류 카테고리, 사용자 기록 
    
class Weather(models.Model):
    # 날짜, 지역, API 응답
    date = models.DateTimeField()
    region =  models.CharField(max_length=10)
    content = models.TextField()


# top, outer, bottom, onepiece, shoes, headwear
class clothing_top(models.Model):
    name = models.CharField(max_length=10)
    
# class UserRecords(models.Model):
    # 사용자 ID(외래키), 날짜, 해당 기상 데이터(외래키), 
    # top, outer, bottom, onepiece, shoes, headwear
#    pass
    