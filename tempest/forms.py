from .models import ClotheRecords
from django import forms 

class RecordForm(forms.ModelForm):
    outer = forms.ChoiceField(required=True, label= '아우터', choices = (
        ("1", "롱패딩"),
        ("2", "숏패딩"),
        ("3", "코트"),
        ("4", "무스탕")
    ))
    
    top = forms.ChoiceField(required=True, label= '상의', choices = (
        ("1", "니트"),
        ("2", "맨투맨"),
        ("3", "후드"),
        ("4", "긴팔")
    ))
    
    bottom = forms.ChoiceField(required=True, label= '하의', choices = (
        ("1", "데님"),
        ("2", "슬랙스"),
        ("3", "면바지"),
        ("4", "레깅스")
    ))
    
    etc = forms.ChoiceField(required=True, label= '액세서리', choices = (
        ("1", "장갑"),
        ("2", "캡"),
        ("3", "비니"),
        ("4", "목도리")
    ))
    
    user = forms.CharField(label=("사용자"))
    weather =  forms.CharField(label=("기상"))
        
    class Meta: 
        model = ClotheRecords
        fields = [ 'outer', 'top', 'bottom', 'etc', 'user', 'weather']