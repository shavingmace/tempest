from django.shortcuts import render
from django.http import HttpResponse
from jsonrpc import jsonrpc_method



# Create your views here.

def test(req):
    return HttpResponse("Tempest 시험 가동")

def index(req):
    return HttpResponse("안녕 템페스트")



@jsonrpc_method('test', authenticated=False, safe=False, validate=False)
def testit(req):
    print('rpc 호출')
    print(req)
    data = {
        'name': "난 통신할 거야"
    }
    return data