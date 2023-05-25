from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User




def sign_up(request):
    if request.method =="POST":
        username  = request.POST.get('username')
        password  = request.POST.get('pass1')
        password2  = request.POST.get('pass2')
        email     = request.POST.get('email')
        fName     = request.POST.get('fName')
        lName     = request.POST.get('lName')
        print(username,password,password2,email,fName,lName)
        if password ==password2:
            user = User.objects.create_user(username=username,email=email,password=password)
            user.first_name = fName
            user.last_name = lName
            user.save()
            user1 = authenticate(request=request,username=username,password=password)
            if user1 is not None:
                login(request,user1)
                messages.success(request=request,message="New user succesfully created")
                return redirect("home")
        else:
            messages.success(request,"Enter the same password please")
            return render(request,"signup.html")
    return render(request,"signup.html")
def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    # add logout functionality
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # if user.is_active:
            login(request, user)
            #return redirect('home')  # Redirect to the desired page after successful login
            return redirect("home")
        else:
            messages.success(request=request,message="incorrect user name or password")
            return redirect(login_view)
    else:
        return render(request , 'login.html', {})

def logout_user(request):
    logout(request=request)
    return redirect("login")
