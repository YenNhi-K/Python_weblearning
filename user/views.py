from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
import english_test
from .models import User
from .forms import UserRegisterForm, UserLoginForm, UserChangePasswordForm
from english_test.models import Test, History
from dictionary.models import Dictionary

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
            })
        
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {
        'form': form
    })

def login(request):
    if 'user_id' in request.session:
        return redirect(reverse('index'))
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_query = User.objects.filter(username=username, password=password)
            if user_query.exists():
                user = user_query.get()
                request.session['user_id'] = user.user_id
                request.session['username'] = user.username
                return index(request)
            else:
                print(username, password)
    else:
        form = UserLoginForm()
    return render(request, 'user/login.html', {'form': form})

def logout(request):
    del request.session['user_id']
    del request.session['username']
    return redirect(reverse('login'))

def change_password(request):
    if 'user_id' not in request.session:
        return redirect(reverse('login'))
    if request.method == 'POST':
        form = UserChangePasswordForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            password = form.cleaned_data['new_password']
            user_query = User.objects.filter(username=request.session['username'], password=current_password)
            if user_query.exists():
                user_query.update(password=password)
                return logout(request)
            else:
                form.add_error("current_password", 'Mật khẩu hiện tại không đúng')
    else:
        form = UserChangePasswordForm()
    return render(request, 'user/change_password.html', {'form': form})

def file(request):
    if request.method == 'POST':
        return redirect(reverse('english_test:import_file'), request=request)

def test(request):
    if request.method == 'POST':
        return redirect(reverse('english_test:test'), request=request)

def list_test(request):
    if 'user_id' not in request.session:
        return redirect(reverse('login'))
    user_id = request.session["user_id"]
    username = User.objects.filter(user_id=user_id).first().username
    test_list = list(Test.objects.filter(user_id=user_id))
    return render(request, 'user/list.html', {'list': test_list, 'username': username})

def voca_list(request, test_id):
    test = Test.objects.filter(test_id=test_id).first()
    list_dictionary = list(Dictionary.objects.filter(test=test))
    return render(request, 'user/voca_list.html', {'list': list_dictionary, 'test': test})

def history(request, test_id):
    test = Test.objects.filter(test_id=test_id).first()
    list_history = list(History.objects.filter(test=test))
    return render(request, 'user/history.html', {'list': list_history, 'test': test})

def delete_test(request):
    if request.method == 'POST':
        test_id = request.POST.get('test_id',None)
        test = Test.objects.filter(test_id=test_id).first()
        test.delete()
    return redirect(reverse('list'))

def index(request):
    if 'user_id' in request.session:
        url = reverse('home')
        print(url)
        return redirect(reverse('home'))
    else:
        return redirect(reverse('login'))   