# Import necessary modules and models
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import ComplaintForm

def home(request):
    return render(request, 'home.html')

def login_page(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/')
        
        user = authenticate(username=username, password=password)
        
        if user is None:
    
            messages.error(request, "Invalid Password")
            return redirect('/')
        else:

            login(request, user)
            return redirect('/home/')
    
    return render(request, 'login.html')

# Define a view function for the registration page
def register_page(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        

        user = User.objects.filter(username=username)
        
        if user.exists():
            messages.info(request, "Username already taken!")
            return redirect('/register/')
        
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        

        user.set_password(password)
        user.save()
        
        messages.info(request, "Account created Successfully!")
        return redirect('/register/')
    
    return render(request, 'register.html')


@login_required
def submit_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            return redirect('/my-complaints/')
    else:
        form = ComplaintForm()
    return render(request, 'submit_complaint.html', {'form': form})

@login_required
def user_complaints(request):
    complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user_complaints.html', {'complaints': complaints})