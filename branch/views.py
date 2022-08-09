from email import message
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Report,User,Topic,Comment
from .form import Editcomment, ReportCreationForm,Creationform,ProfileEdit
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def loginuser(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            return render(request,'loginuser.html',{'error':'User doest exists','pages':'login'})
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return render(request,'loginuser.html',{'error':'Enter correct password ','pages':'login'})
    return render(request,'loginuser.html',{'pages':'login'})
def logoutuser(request):
    logout(request)
    return redirect('home')

def register(request):
    form=Creationform()
    dict={'form':form}
    if request.method=='POST':
        dict1={'form':form,'error':"Passwords are't same "}
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        try:
            if pass1 == pass2 :
                form=Creationform(request.POST)
                user=form.save(commit=False)
                user.set_password(pass1)
                user.save()
                login(request,user)
                return redirect('home')
            else:
                return render(request,'loginuser.html',dict1)
        except:
            dict1={'form':form,'error':"Username already exist "}
            return render(request,'loginuser.html',dict1)
    
    return render(request,'loginuser.html',dict)

def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ""
    report=Report.objects.filter(Q(topic__topic__icontains=q)|
                                 Q(headlines__icontains=q)|
                                 Q(description__icontains=q))
    comment=Comment.objects.filter(Report__topic__topic__icontains=q)
    report_count=report.count()
    topic=Topic.objects.all()
    dict={'reports':report,'topics':topic,'report_count':report_count,'comments':comment}
    return render(request,'home.html',dict)


def report(request,number):
    
    report=Report.objects.get(id=number)
    comments=report.comment_set.all()
    participents=report.participents.all()
    topic=Topic.objects.all()
    if request.method=="POST":
        comments=Comment.objects.create(
            name=request.user,
            Report=report,
            body=request.POST.get('comment')
        )
        report.participents.add(request.user)
        return redirect('report',number=number)
    dict={'reports':report,'comments':comments,'participents':participents,'topics':topic}
    return render(request,'report.html',dict)
@login_required(login_url='loginuser')
def createreport(request):
    form=ReportCreationForm()
    if request.method=='POST':
        form=ReportCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.host=request.user
            user.save()
            return redirect('home')
    dict={'form':form}
    return render(request,'createreport.html',dict)


@login_required(login_url='loginuser')
def editreport(request,number):
    report=Report.objects.get(id=number)
    form=ReportCreationForm(instance=report)
    if request.method=='POST':
        form=ReportCreationForm(request.POST,instance=report)
        if form.is_valid():
            form.save()
            return redirect('home')
    dict={'form':form}
    return render(request,'editreport.html',dict)


@login_required(login_url='loginuser')
def deletereport(request,number):
    report=Report.objects.get(id=number)
    if request.method=='POST':
        report.delete()
        return redirect('home')
    dict={'reports':report}
    return render(request,'delete.html',dict)

@login_required(login_url='loginuser')
def editcomment(request,number):
    message=Comment.objects.get(id=number)
    form=Editcomment(instance=message)
    if request.method=="POST":
        form=Editcomment(request.POST,instance=message)
        form.save()
        return redirect('report',number=message.Report.id)
    dict={'form':form}
    return render(request,'editcomment.html',dict)

@login_required(login_url='loginuser')
def deletecomment(request,number):
    message=Comment.objects.get(id=number)
    if request.method=="POST":
        message.delete()
        return redirect('report',number=message.Report.id)
    form={'message':message}
    return render(request,'delete.html',form)


def profile(request,number):
    user=User.objects.get(id=number)
    reports=user.report_set.all()
    topics=Topic.objects.all()
    comments=user.comment_set.all()
    report_count=reports.count()
    dict={'reports':reports,'topics':topics,'comments':comments,'users':user,'report_count':report_count}
    return render(request,'profile.html',dict)

def editprofile(request,number):
    user=User.objects.get(id=number)
    form=ProfileEdit(instance=user)
    dict={'form':form}
    if request.method=="POST":
        auth=authenticate(request,username=request.user.username,password=request.POST.get('pass1'))
        if auth is not None:
            form=ProfileEdit(request.POST,instance=user)
            if form.is_valid():
                form.save()
                return redirect('profile',number=request.user.id)
        else:
            dict={'form':form,'error':'password is wrong'}
            return render(request,'editprofile.html',dict)
    
    return render(request,'editprofile.html',dict)