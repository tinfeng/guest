from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event


# Create your views here.
def index(request):
    return render(request, "index.html")


def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            response = HttpResponseRedirect('/event_manage/')
            request.session['user'] = username     # 将username写到浏览器session里
            return response
        elif username is '':
            return render(request, 'index.html', {'error': 'username is not None!'})
        elif password is '':
            return render(request, 'index.html', {'error': 'password is not None!'})
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})


# 发布会管理
@login_required
def event_manage(request):
    # username = request.COOKIES.get('user', '')    #浏览器获取cookie
    event_list = Event.objects.all()
    username = request.session.get('user', '')      # 浏览器获取session
    return render(request, "event_manage.html", {"user": username, "events": event_list})
