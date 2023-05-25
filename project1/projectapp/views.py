from django.shortcuts import render,redirect
from django.http import HttpResponse
from login.models import attendance,leave
import datetime
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        now = datetime.datetime.now()
        start_date = datetime.datetime(now.year, now.month, 1).date() 
        end_date = now.date() 
        presents = attendance.objects.filter(user=request.user, date__range=[start_date, end_date]).count()
        if presents >= 26:
            grade = 'A'
        elif presents >=20:
            grade ='B'
        elif presents >= 15:
            grade= 'C'
        else:
            grade = 'D'


        return render(request,"home.html",{"name" : request.user.username,"grade":grade})
    else:
        return redirect("login")
    
    
def markAttendance(request):
    if request.user.is_authenticated:
        att = attendance.objects.filter(user= request.user)
        for attendances in att:
            if attendances.date == datetime.date.today():
                res = f"{request.user.first_name} your  attendance for {datetime.date.today()} was already  marked"
                return HttpResponse(res) 
        data = {
            "user" : request.user,
            "date": datetime.date.today()
        }
        instance = attendance(**data)
        instance.save()
        res = f"{request.user.first_name} your  attendance for {datetime.date.today()} has been marked"
        return HttpResponse(res)
    else:
        return redirect("login")

    
def markLeave(request):
    if request.user.is_authenticated:
        le = leave.objects.filter(user= request.user)
        for leaves in le:
            if leaves.date == datetime.date.today():
                res = f"{request.user.first_name} your  leave for {datetime.date.today()} was already  marked"
                return HttpResponse(res) 
        data = {
            "user" : request.user,
            "date": datetime.date.today(),
            "status":"pending"
        }
        instance = leave(**data)
        instance.save()
        res = f"{request.user.first_name} your  leave for {datetime.date.today()} has been marked please wait for approval"
        return HttpResponse(res)
    else:
        return redirect("login")

def viewAttendance(request):
    if request.user.is_authenticated:
        now = datetime.datetime.now()
        start_date = datetime.datetime(now.year, now.month, 1).date() 
        end_date = now.date() 
        totalDays = (end_date - start_date).days + 1

        att = attendance.objects.filter(user=request.user, date__range=[start_date, end_date])

        presents = [attendance.date for attendance in att]
        attendance_data = []
        for i in range(totalDays):
            current_date = start_date + datetime.timedelta(days=i)
            is_present = current_date in presents
            
            data = {
                "date": current_date,
                "present": is_present
            }
            attendance_data.append(data)

        leaves = leave.objects.filter(user=request.user, date__range=[start_date, end_date])
        leaveData = [{"date": l.date, "status": l.status} for l in leaves]
        context = {
            "name":request.user.username,
            "attendance":attendance_data,
            "leaves": leaveData
        }
        return render(request,"view.html",context)

    else:
        return redirect("login")


        return render(request,'adminPanel.html',{"name":request.user.username})

def adminPanel(request):

    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == "POST":
                start = request.POST.get('startDate')
                end = request.POST.get('endDate')
                username = request.POST.get('username')

                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    messages.success(request, "Invalid username")
                    return render(request, 'adminPanel.html')

                start_date = datetime.datetime.strptime(start, '%Y-%m-%d').date()
                end_date = datetime.datetime.strptime(end, '%Y-%m-%d').date()
                totalDays = (end_date - start_date).days + 1

                att = attendance.objects.filter(user=user, date__range=[start_date, end_date])
                presents = [attendance.date for attendance in att]

                attendance_data = []
                for i in range(totalDays):
                    current_date = start_date + datetime.timedelta(days=i)
                    is_present = current_date in presents

                    data = {
                        "date": current_date,
                        "present": is_present
                    }
                    attendance_data.append(data)

                leaves = leave.objects.filter(user=user, date__range=[start_date, end_date])
                leaveData = [{"date": l.date, "status": l.status} for l in leaves]

                context = {
                    "attendance": attendance_data,
                    "leaves": leaveData,
                    "name": request.user.username
                }

                
                return render(request, 'adminPanel.html', context)

            else:
                return render(request, 'adminPanel.html', {"name": request.user.username})

    return redirect('login')
