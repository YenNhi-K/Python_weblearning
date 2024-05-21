from django.shortcuts import render,redirect
from django.urls import reverse
from .models import Test, History
from dictionary.models import Dictionary
from user.views import home
from user.models import User
import pandas as pd
from django.http import HttpResponse
import random


from django.core.cache import cache
# Create your views here.

def import_file(request):
    if request.method == 'POST':
        # print(request.FILES)
        topic = request.POST.get('topic',None)
        file = request.FILES['file']
        if file.name.endswith('.csv'):
            df = pd.read_csv(file, header=None)
        elif file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file, header=None)
        
        user = User.objects.filter(user_id=request.session["user_id"]).first()

        test = Test(user=user, number_of_words=len(df), topic=topic)
        test.save()
        # test_id = test.test_id
        for index, row in df.iterrows():
            dict = Dictionary(test=test, word=row[0], meaning=row[1])
            dict.save()
        return redirect(reverse('home'))
    
def check(request):
    if request.method == 'POST':
        number_of_questions = request.POST.get('number_of_questions', None)
        test_id = request.POST.get('test_id', None)
        cache.set('test_id', test_id)
        print(number_of_questions, test_id)
        test = Test.objects.filter(test_id=test_id).first()
        list_dictionary = list(Dictionary.objects.filter(test=test))
        # print(list_dictionary)
        list_question = []
        if test.number_of_words >= int(number_of_questions):
            random.shuffle(list_dictionary)
            for _ in range(int(number_of_questions)):
                word_or_meaning = random.randint(0,1)
                if word_or_meaning == 0:
                    list_question.append({
                        'question': list_dictionary[_].word,
                        'answer': list_dictionary[_].meaning,
                        'type': 0
                    })
                else:
                    list_question.append({
                        'question': list_dictionary[_].meaning,
                        'answer': list_dictionary[_].word,
                        'type': 1
                    })
        else:
            times = int(number_of_questions) / test.number_of_words 
            for _ in range (times):
                random.shuffle(list_dictionary)
                for _ in range(int(number_of_questions)):
                    word_or_meaning = random.randint(0,1)
                    if word_or_meaning == 0:
                        list_question.append({
                            'question': list_dictionary[_].word,
                            'answer': list_dictionary[_].meaning,
                            'type': 0,
                        })
                    else:
                        list_question.append({
                            'question': list_dictionary[_].meaning,
                            'answer': list_dictionary[_].word,
                            'type': 1,
                        })
        cache.set('list_question', list_question)
        return list_question
def remove_element_from_list(my_list, element):
    # Sử dụng vòng lặp để loại bỏ tất cả các phần tử có giá trị 'a' khỏi danh sách
    while element in my_list:
        my_list.remove(element)
def quiz(request):
    if request.method == 'POST':
        number_of_questions = request.POST.get('number_of_questions', None)
        test_id = request.POST.get('test_id', None)
        cache.set('test_id', test_id)
        # print(number_of_questions, test_id)
        test = Test.objects.filter(test_id=test_id).first()
        list_dictionary = list(Dictionary.objects.filter(test=test))
        list_choice_words = [item.word for item in list_dictionary]
        list_choice_meanings = [item.meaning for item in list_dictionary]
        # print(list_dictionary)
        list_question = []
        while(len(list_choice_words) < 4):
            list_choice_words.append(" ")
        while(len(list_choice_meanings) < 4):
            list_choice_meanings.append(" ")
        if test.number_of_words >= int(number_of_questions):
            random.shuffle(list_dictionary)
            for _ in range(int(number_of_questions)):
                word_or_meaning = random.randint(0,1)
                if word_or_meaning == 0:
                    list_choice = [element for element in list_choice_meanings if element != list_dictionary[_].meaning]
                    random_choice = random.sample(list_choice, 3)
                    random_choice.append(list_dictionary[_].meaning)
                    list_question.append({
                        'question': list_dictionary[_].word,
                        'answer': list_dictionary[_].meaning,
                        'list_choice': random_choice,
                        'type': 0
                    })
                else:
                    list_choice = [element for element in list_choice_words if element != list_dictionary[_].word]
                    random_choice = random.sample(list_choice, 3)
                    random_choice.append(list_dictionary[_].word)
                    list_question.append({
                        'question': list_dictionary[_].meaning,
                        'answer': list_dictionary[_].word,
                        'list_choice': random_choice,
                        'type': 1
                    })
        cache.set('list_question', list_question)
        return list_question


def test_check(request, no_question, no_correct=0):
    list_question = cache.get('list_question')
    print(list_question)
    correct = None
    # print(no_question, len(list_question))
    question = None
    # print(question)
    user_answer = ""
    if no_question == len(list_question):
        test_id = cache.get('test_id')
        test = Test.objects.filter(test_id=test_id).first()
        user = User.objects.filter(user_id=request.session['user_id']).first()
        history = History(
            test=test,
            user=user,
            result=no_correct,
            number_of_questions=len(list_question),
            type=0
        )
        history.save()
        return render(request, 'test/result.html', {'number_of_questions': len(list_question), 'no_correct': no_correct})
    else:
        question = list_question[no_question]
        if request.method == 'POST':
            user_answer = request.POST.get('answer', "")
            print(user_answer)
            
            if user_answer == question['answer']:
                correct = 0
            else:
                correct = 1
    
    return render(request, 'test/check_game.html', {'question': question, 'no_question': no_question, 'no_correct': no_correct, 'correct': correct, 'user_answer': user_answer})
    
def quiz_check(request, no_question, no_correct=0):
    list_question = cache.get('list_question')
    print(list_question)
    correct = None
    # print(no_question, len(list_question))
    question = None
    # print(question)
    user_answer = ""
    if no_question == len(list_question):
        test_id = cache.get('test_id')
        test = Test.objects.filter(test_id=test_id).first()
        user = User.objects.filter(user_id=request.session['user_id']).first()
        history = History(
            test=test,
            user=user,
            result=no_correct,
            number_of_questions=len(list_question),
            type=1
        )
        history.save()
        return render(request, 'test/result.html', {'number_of_questions': len(list_question), 'no_correct': no_correct, 'correct': correct, 'user_answer': user_answer})
    else:
        question = list_question[no_question]
        if request.method == 'POST':
            user_answer = request.POST.get('selected_option', "")
            if user_answer == question['answer']:
                correct = 0
            else:
                correct = 1
            # print(correct)
            print(question)
    return render(request, 'test/quiz_game.html', {'question': question, 'no_question': no_question, 'no_correct': no_correct, 'correct': correct, 'user_answer': user_answer})
 

def test(request):
    # count = 0
    if request.method == 'POST':
        test_type = request.POST.get('type', None)
        if test_type == 'check':
            list_question = check(request)
            request.method = 'GET'
            return test_check(request, 0)
        elif test_type == 'quiz':
            list_question = quiz(request)
            request.method = 'GET'
            return quiz_check(request, 0)
        # print(list_question)
    # return home(request)
    

def test_home(request):
    return home(request)
