from pyexpat.errors import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, 
    FormView,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.views import (
    LoginView as DjangoLoginView,
    LogoutView as DjangoLogoutView,
)
from django.db import transaction
from user.models import User
from user.forms import (
    LoginForm,
    ProfileForm, 
    RegisterForm, 
    UserForm,
)

from django.shortcuts import redirect, render

def my_blog(request):
    return render(request, "index.html")


class RegisterView(CreateView):
    template_name = "register.html"
    form_class = RegisterForm
    model = User
    success_url = reverse_lazy("home")

    def form_valid(self, form: RegisterForm) -> HttpResponse:
        res = super().form_valid(form)
        login(self.request, form.instance)
        return res

class LoginView(DjangoLoginView):
    form_class = LoginForm
    template_name = "login.html"


class logoutView(DjangoLogoutView):
    pass


@transaction.atomic
def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })