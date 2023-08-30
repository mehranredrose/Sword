from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserSW, CustomUser
from django.db.models import Q
#from .templates.forms import *
from .forms import *
import random

#render home screen as default
def index(request):
    #return render(request, 'safe_word/home.html')
    return render(request, 'index.html')
def home(request):
    if request.user.is_authenticated:
        logged_in_user = request.user  
    return render(request, 'home.html',{'user': logged_in_user})


def register_page(request):
    #Use the Registration form from forms.py
    form = RegisterForm(request.POST or None)
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in as  %s " % request.user + " you can't register or login ones already logged in!")
        return redirect(index)
        #check if valid if so create a user otherwise raise an exception
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        try:
            user = CustomUser.objects.create_user(username, email, password)
        except:
            user = None
        if user != None:
            login(request, user)
            return redirect(all_passwords)
        else:
            request.session['register_error'] = 1 # 1 == True
    #return render(request, "safe_word/user_account/register.html", {"form": form})
    return render(request, "user_account/register.html", {"form": form})


def login_page(request):
    form = LoginForm(request.POST or None)
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in as %s" % request.user + " you can't register or login ones already logged in!")
        return redirect(all_passwords)
    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        user = authenticate(request, email=email, password=password)
        if user != None:
            login(request, user)
            return redirect(all_passwords)
        else:
            messages.warning(request, 'Please enter the right password!')
    return render(request, "user_account/login.html", {"form": form})

  
#The @login_required decorator checks if user is logged in otherwise you can't access the logout page.
@login_required(login_url=login_page)
def logged_out_page(request):
    logout(request)
    #return render(request, "safe_word/user_account/logged_out.html")
    return render(request, "user_account/logged_out.html")


@login_required(login_url=login_page)
def all_passwords(request):
    if request.user.is_authenticated:
        messages.success(request, "Logged in as %s" % request.user)
    logged_in_user = request.user  
    logged_in_user_pws = UserSW.objects.filter(user=logged_in_user).order_by('-date')
    if not logged_in_user_pws:
        message = 'Please create a password'
        #return render(request, "safe_word/user_password/user_pw_all.html", {'no_pws': message})
        return render(request, "user_password/all_passwords.html", {'no_pws': message})
    
    #return render(request, "safe_word/user_password/user_pw_all.html", {'pws': logged_in_user_pws})
    return render(request, "user_password/all_passwords.html", {'pws': logged_in_user_pws})

    
@login_required
def edit_post(request, pk):
    user_post = UserSW.objects.get(id=pk)
    form = UserUpdateForm(instance=user_post)
    
    if request.method == 'POST':
        form =UserUpdateForm(request.POST, instance=user_post)
        if form.is_valid():
            form.save()
            return redirect(all_passwords)
    
    context = {'form': form}

    #return render(request, 'safe_word/user_password/edit.html', context)
    return render(request, 'user_password/edit.html', context)


@login_required
def delete(request, pk):
    user_post = UserSW.objects.get(id=pk)
    
    if request.method == 'POST':
        user_post.delete()
        return redirect(all_passwords)
    
    context = {'item': user_post} 

    #return render(request, 'safe_word/user_password/delete.html', context)
    return render(request, 'user_password/delete.html', context)

@login_required(login_url=login_page)
def add_password(request):
    form = UserSWForm(request.POST or None)
    if request.user.is_authenticated:
        messages.success(request, "Logged in as %s" % request.user)
    logged_in_user = request.user
    if form.is_valid():
        title = form.cleaned_data.get("title")
        password = form.cleaned_data.get("password")
        type = form.cleaned_data.get("type")
        if UserSW.objects.filter(title=title) and UserSW.objects.filter(user=request.user):
            messages.success(request, "---There is already a password created by that name---")
        else:
            try:
                UserSW.objects.create(title=title, password=password, type=type, user=logged_in_user)
                messages.success(request, "---Successfully added new password field for your storage---")
                return redirect(all_passwords)
            except Exception as e:
                raise e
            
    #return render(request, "safe_word/user_password/user_pw_add.html", {'form': form})
    return render(request, "user_password/add_password.html", {'form': form})
 
@login_required(login_url=login_page)
def search_passwords(request):
    if request.user.is_authenticated:
        messages.success(request, "Logged in as %s" % request.user)
    logged_in_user = request.user  
    logged_in_user_pws = UserSW.objects.filter(user=logged_in_user)
    if request.method == "POST":
        searched = request.POST.get("password_search", "")
        users_pws = logged_in_user_pws.values()
        if users_pws.filter(title=searched):
            user_pw = UserSW.objects.filter(Q(title=searched)).values()
            return render(request, "safe_word/user_password/search_passwords.html", {'user_pw': user_pw})
        else:
            messages.error(request, "---YOUR SEARCH RESULT DOESN'T EXIST---")
   

    #return render(request, "safe_word/user_password/user_pw_search.html", {'pws': logged_in_user_pws})
    return render(request, "user_password/search_passwords.html", {'pws': logged_in_user_pws})


@login_required(login_url=login_page)
def generate(request):
    
    try:    
        characters = list()

        if request.GET.get('uppercase'):
            characters.extend(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
        
        if request.GET.get('lowercase'):
            characters.extend(list('abcefghijklmnopqrstuvwxyz'))    

        if request.GET.get('special'):
            characters.extend(list('~!@#$%^&*()_+="\/|?><.:;'))
        
        if request.GET.get('numbers'):
            characters.extend(list('0123456789'))

        length = int(request.GET.get('length', 14))

        the_password = ''
        
        for x in range(length):
            the_password += random.choice(characters)
        massage=None
    except:
        the_password = None
        massage='You Should Select Option First'

    return render(request, 'user_password/password_generator.html', {'password': the_password,'massage': massage})

def about(request):
    #return render(request, 'safe_word/home.html')
    return render(request, 'about.html')