from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.views.generic import ListView
from django.contrib import messages
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from Notes.models import Activity
from .forms import UserRegistrationForm, ProfileForm


# Create your views here.

def updateUser(request):
    user = request.user
    profile = user.profile
    form = UserRegistrationForm(instance=profile)
    p_form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, instance=profile)
        if form.is_valid() and p_form.is_valid():
            p_form.save()
            form.save()
            Activity.objects.create(author=user, title='Updated Profile', body='Updated Profile')
            messages.success(request, 'Profile updated successfully')
            return redirect('home')
    context = {
        'form':form
    }
    return render(request, 'userupdate.html', context)

def login_form(request):
    context = {
        'title':'Login'
    }
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            # subject, from_email, to = 'Login Alert', 'codingfoxblogs@gmail.com', f'{user.email}'
            # text_content = 'This is an important message.'
            # html_content = f'<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">\n<head><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200&display=swap" rel="stylesheet">\n<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="x-apple-disable-message-reformatting"><title></title></head<body style="margin:0;padding:0;font-family:"Poppins",Arial,sans-serif;"><table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;background:#ffffff;"><tr><td align="center" style="padding:0;"><table role="presentation" style="width:602px;border-collapse:collapse;border:1px solid #cccccc;border-spacing:0;text-align:left;"><tr><td align="center" style="padding:40px 0 30px 0;background:#efefef;"><h1>Coding<span style="background-color: transparent; color: #0076d1;text-decoration: none;">Fox</span> Blogs</h1></td></tr><tr><td style="padding:36px 30px 42px 30px;"><table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;"><tr><td style="padding:0 0 36px 0;color:#153643;"><h1 style="font-size:24px;margin:0 0 20px 0;font-family:Arial,sans-serif;">Login Alert Mail</h1><p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;">This is to tell you that your account with username: {username} signing in at {datetime.now()}, If this is not you please consider changing your password immediately!</p><h3 style="margin:0;line-height:24px;font-family:Arial,sans-serif;"><a href="https://codingfox.pythonanywhere.com/users/password-reset/" style="padding: 1%; background-color: #0076d1; color: white;text-decoration: none;">Reset Password!</a></h3><br><p>Please do not reply to this email address, Mail me here: <a href="mailto:ketanv288@gmail.com" style="background-color: transparent; color: #0076d1;text-decoration: none;">Mail Me!</a></p></td></tr></table></body></html>'
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()
            return redirect('home')
        else:
            messages.error(request, f'Account Does Not Exists with {username}')
            return render(request, 'login.html', context)
    return render(request, 'login.html', context)

def logout_form(request):
    context = {
        'title':'Logout'
    }
    logout(request)
    return render(request, 'logout.html', context)

def registeration_form(request):
    if request.method == 'POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request,f'Account created for {username}! Just Login')
            # messages.warning(request,f'Upon Regiestering you are agreeing with the using required cookies')
            # subject, from_email, to = f'Welcome {username}', 'codingfoxblogs@gmail.com', f'{email}'
            # text_content = 'This is an important message.'
            # html_content = (f'<div style="background-color: hsl(206, 98%, 90%);color: #363636;width: 90%;height: auto;font-weight: 300;padding: 5%;"><h1 style="text-align:center;">Welcome {username}!</h1><br><h3> Explore the website CodingFox Blogs, you can also create Blogs on this blog page at no cost<br><a href="https://codingfox.pythonanywhere.com/" style="padding: 1%; background-color: #0076d1; color: white;text-decoration: none;">Explore More!</a></h3><br><p>Please do not reply to this gmail, if you want to contact mail here for any query <a href="mailto:ketanv288@gmail.com">📧Mail Me</a></p></div>')
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()
            return redirect('login')
    else:
        form=UserRegistrationForm()
    context = {
        'title':'Register',
        'form':form
    }
    return render(request,'newuser.html',context)
