from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
import english_test
from .models import User
from .forms import UserRegisterForm, UserLoginForm
from english_test.models import Test

# Create your views here.

def home(request, error=None):
    if 'user_id' not in request.session:
        return redirect(reverse('login'))
    user_id = request.session["user_id"]
    username = User.objects.filter(user_id=user_id).first().username
    print(username)
    test_list = list(Test.objects.filter(user_id=user_id))
    return render(request, 'user/home.html', {'list': test_list, 'username': username})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = User(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password']
            )
            new_user.save()
            print(new_user.user_id)
            return render(request, 'user/login.html', {
                'form': UserLoginForm(),
                # 'success': True
            })
        
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {
        'form': form
    })

def login(request):
    if 'user_id' in request.session:
        return redirect(reverse('home'))
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_query = User.objects.filter(username=username, password=password)
            if user_query.exists():
                user = user_query.get()
                request.session['user_id'] = user.user_id
                # request.session['username'] = user.username
                # return render(request, 'user/home.html')
                return index(request)
            else:
                print(username, password)
    else:
        form = UserLoginForm()
    return render(request, 'user/login.html', {'form': form})
def logout(request):
    del request.session['user_id']
    return redirect(reverse('login'))

def import_file(request):
    if request.method == 'POST':
        topic_value = request.POST.get('topic', None)
        if not topic_value:
            return redirect(reverse('home', kwargs={'error': 'Nhập tên topic'}))
        return redirect(reverse('english_test:import_file'), request=request)
    # else:

def test(request):
    if request.method == 'POST':
        return redirect(reverse('english_test:test'), request=request)
def index(request):
    # return render(request, 'user/home.html')
    if 'user_id' in request.session:
        return redirect(reverse('home'))
    else:
        return redirect(reverse('login'))   