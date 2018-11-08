from django.shortcuts import render

from django.views.generic.base import View
# Create your views here.

class LoginView(View):
    def get(self, request):
        print("a")
        return render(request, "login.html", {})

def login_chen(request):
    if request.method == "POST":
        pass
    elif request.method == 'GET':
        return render(request,"login.html",{})


class IndexView(View):
    #慕学在线网 首页
    def get(self, request):
        #取出轮播图

        return render(request, 'index.html', {

        })


