from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import TempestUser

class UserForm(UserCreationForm):
    #ID, PW, 지역, 젠더, 연령
    # gender 
    error_messages = {
        'password_mismatch': "The two password fields didn't match."
    }
    password1 = forms.CharField(label=("비밀번호"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=("비밀번호 확인"), 
                                widget=forms.PasswordInput, 
                                help_text=("같은 비밀번호를 입력하세요."),
                                )
    gender = forms.ChoiceField(required=True, label= '젠더', choices = (
        ("1", "여성"),
        ("2", "남성"),
        ("3", "논바이너리"),
        ("4", "응답하지 않음"),
    ))
    
    region = forms.ChoiceField(required=True, label= '지역', choices=(
        ("1", "강원도"),
        ("2", "경기도"),
        ("3", "경상남도"),
        ("4", "경상북도"),
        ("5", "전라남도"),
        ("6", "전라북도"),
        ("7", "제주도"),
        ("8", "충청남도"),
        ("9", "충청북도"),
    ))
    
    age = forms.ChoiceField(required=True, label= '나이', choices=(
        ("1", "10대"),
        ("2", "20대"),
        ("3", "30대"),
        ("4", "40대"),
        ("5", "50대"),
        ("6", "60대"),
        ("7", "70대"),
        ("8", "80대"),
        ("9", "90대"),
    ))
    
    class Meta: 
        model = TempestUser
        fields = ("username", "region", "gender", "age")
        
