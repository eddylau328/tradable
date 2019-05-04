from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.

#it is used to render the register page.
def user_register_view(request):
    if request.method == 'POST':
        # By sending a form to the frontend, it can let the user to input the required data for the registration.
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # After submitting the form at the frontend by the user, it will send a POST request to the backend. And it will check whether the form is valid or not. If the form is valid, it will save it to the database.
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You can log in now!')
            return redirect('login')
    else:
        form = UserRegisterForm()

    context = {
        'form': form
    }
    return render(request, 'user/register.html', context)

# it uses two forms for user to input the data.
@login_required
def user_profile_view(request):
    if request.method == 'POST':
        # The u_form is used to correct the user data. The p_form is used to correct the profile picture.
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            # After submitting the finished forms by the user, it will save the two forms to update the data.
            u_form.save()
            p_form.save()
            # a success message will appear.
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'user/profile.html', context)
