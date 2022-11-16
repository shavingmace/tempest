from .models import ClotheRecords
from django import forms
from django.utils.safestring import mark_safe


def make_choices(ls: list):
    choices = []
    for ix, elem in enumerate(ls):
        choices.append((str(ix+1), elem))
    return choices 


class RecordForm(forms.ModelForm):
    #outer_ls = ['후드집업', '플리스/뽀글이', '무스탕', '롱패딩', '자켓/블레이저', '코트', '야상', '트렌치코트', '가죽자켓', '숏패딩', '블루종', '가디건']
    #top_ls = ['후드티셔츠', '맨투맨/스웨트셔츠', '니트/스웨터', '셔츠/블라우스', '반소매 티셔츠', '긴소매 티셔츠', '민소매 티셔츠']
    #bottom_ls = ['원피스', '스커트', '슬랙스', '레깅스', '면바지', '반바지', '청바지']
    #etc_ls = ['버킷햇', '비니', '캡 모자', '목도리', '장갑']
    #outer = forms.ChoiceField(required=True,  choices = make_choices(outer_ls), widget=forms.RadioSelect)
    #top = forms.ChoiceField(required=True,  choices = make_choices(top_ls), widget=forms.RadioSelect)
    #bottom = forms.ChoiceField(required=True,  choices = make_choices(bottom_ls), widget=forms.RadioSelect)
    #etc = forms.ChoiceField(required=True,  choices = make_choices(etc_ls), widget=forms.RadioSelect)
    #user = forms.CharField(label=("사용자"))
    #weather =  forms.CharField(label=("기상"))
    
    class Meta:     
        model = ClotheRecords
        fields = [ 'user', 'weather', 'clothes']
        #labels = { 'outer':'아우터', 'top':'상의', 'bottom':'하의', 'etc':'악세서리' }
        
