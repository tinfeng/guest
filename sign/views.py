from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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

# 发布会名称搜索
@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user": username, "events": event_list, "search": search_name})

# 嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果输入的数字不是整数,取第一页数据
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果输入的数字不在范围内,取最后一页数据
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username, "guests": contacts})

