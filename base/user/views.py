from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from base.user.forms import *
from base.verifier import user_not_logged_in


@user_passes_test(test_func=user_not_logged_in, login_url='home-url')
def signup_user(request):
    """Controls the app's landing page"""

    if request.method == "POST":
        # Create user, associate user with farm
        user_form = CustomUserCreationForm(request.POST, request.FILES)
        farm_form = FarmForm(request.POST)

        if farm_form.is_valid() and user_form.is_valid():
            farm = farm_form.save()
            user = user_form.save(commit=False)
            user.farm = farm
            user.save()
            messages.info(request, "Account was created successfully!")
            return redirect('home-url')
        else:
            if farm_form.has_error:
                messages.error(request, farm_form.errors)
                return redirect('home-url')
            if user_form.has_error:
                messages.error(request, user_form.errors)
                return redirect('home-url')
    
    user_form = CustomUserCreationForm()
    farm_form = FarmForm()

    context = {'u_form': user_form, 'f_form': farm_form}
    return render(request, 'signup.html', context)

@user_passes_test(test_func=user_not_logged_in, login_url='home-url')
def login_user(request):
    """Controls user login"""

    if request.method == 'POST':
        # Does user exist?
        user = CustomUser.objects.get(email=request.POST.get('email', None))
        if user:
            # Verify credentials
            user = authenticate(
                email = request.POST.get('email', ''),
                password = request.POST.get('password', '')
                )
            if user:
                # Create user session
                login(request, user)
                return redirect('home-url')
        else:
            messages.error("Invalid email or password!")
            return redirect('home-url')
        
    context = {'form': LoginForm()}
    return render(request, 'login.html', context)

def logout_user(request):
    """Controls user logout"""

    logout(request)
    return redirect('home-url')


def home(request):
    """Renders the app's landing page"""

    users_count = CustomUser.objects.count()
    context = {"users_count": users_count}
    return render(request, 'home.html', context)

