from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from . import models
from . models import *
from django.contrib.auth.models import User
from .forms import ResponseForm, CommentForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required



@login_required
def home(request, num):
    all_ques = Question.objects.all()
    needed = Question.objects.get(q_no=num)
    curr_person = request.user


    if request.method == 'POST':
        form = ResponseForm(request.POST)

        if form.is_valid():
            if Response.objects.filter(question=num, profile=request.user).exists():
                Ans = form.cleaned_data['Ans']
                print(Ans)
                temp = Response.objects.get(question=num, profile=request.user)
                temp.response = Ans
                temp.save()
                return redirect('questions')

            else:
                Ans = form.cleaned_data['Ans']
                print(Ans)
                Response.objects.create(question=needed, profile=curr_person, response=Ans)
                Response.save
                return redirect('questions')


    form = ResponseForm()
    if Response.objects.filter(question=num, profile=request.user).exists():
        link = Response.objects.get(question=num, profile=request.user)
        print(type(link))
        return render(request, 'electra/home.html', {'needed': needed, 'form': form, 'link':link})
    else:
        print('dne')
        return render(request, 'electra/home.html', {'needed': needed, 'form': form})



def landing(request):
    return render(request, 'electra/landing.html')

@login_required
def participant(request):
    participant = User.objects.all()
    return render(request, 'electra/participant_profile.html', {'participant': participant})

@login_required
def administrator(request, num):
    answers = User.objects.get(pk=num)
    profile_details = Response.objects.filter(profile=answers)
    print(profile_details)
    return render(request, 'electra/admins.html', {'profile_details': profile_details, 'answers': answers})

@login_required
def comment(request, num, st):

    user_profile = User.objects.get(pk=st)
    user_response = Response.objects.get(question=num, profile=user_profile)
    cur_profile = Profile.objects.get(user=user_profile)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            if Point.objects.filter(ans=user_response, profile=user_profile, author=request.user).exists():
                print('1')
                comment = form.cleaned_data['comment']
                point = form.cleaned_data['point']
                com = Point.objects.get(ans=user_response, profile=user_profile, author=request.user)
                count = com.points
                cur_profile.score = cur_profile.score-count
                com.comment = comment
                com.points = point
                cur_profile.score =cur_profile.score+point
                print(cur_profile.score)
                cur_profile.save()

                com.save()
                return redirect('/participant')

            else:
                print('2')
                comment = form.cleaned_data['comment']
                point = form.cleaned_data['point']
                Point.objects.create(ans=user_response, profile=user_profile, author=request.user, comment=comment, points=point)
                Point.save
                cur_profile.score = cur_profile.score+int(point)
                print(cur_profile.score)
                cur_profile.save()

                return redirect('/participant')

    form = CommentForm()
    if Point.objects.filter(ans=user_response, profile=user_profile, author=request.user).exists():
        print('de')
        return render(request, 'electra/home.html', {'form': form})
    else:
        print('dne')
        return render(request, 'electra/home.html', {'form': form})

@login_required
def questions(request):
    all_questions = Question.objects.all()
    print(all_questions)
    return render(request, 'electra/question_page.html', {'all_questions': all_questions})

@login_required
def start(request):
    return render(request, 'electra/start.html')

def leaderboard(request):
    all_users = Profile.objects.all().order_by('score').reverse()
    per1 = Profile.objects.all().order_by('-score')[0]
    per2 = Profile.objects.all().order_by('-score')[1]
    per3 = Profile.objects.all().order_by('-score')[2]
    print(per1)
    return render(request, 'electra/leaderboard.html', {'all_users': all_users, 'per1': per1, 'per2': per2, 'per3': per3 })

@login_required
def tutorial(request):
    return render(request, 'electra/tutorial.html')



def update_user_social_data(strategy, *args, **kwargs):
  response = kwargs['response']
  backend = kwargs['backend']
  user = kwargs['user']

  if response['picture']:
    url = response['picture']
    userProfile_obj = Profile.objects.get(user=user)

    userProfile_obj.image = url
    userProfile_obj.save()

@login_required
def logout_view(request):
    logout(request)
    return redirect('landing')