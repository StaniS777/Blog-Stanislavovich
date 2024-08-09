from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView, 
    FormView,
)
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.views import (
    LoginView as DjangoLoginView,
    LogoutView as DjangoLogoutView,
)
from django.db import transaction
from publication.models import Public
from user.models import Follow, Profile, User
from user.forms import (
    LoginForm,
    ProfileForm, 
    RegisterForm, 
    UserForm,
)
from django.db.models.query import QuerySet

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



@login_required
def follow_user(request: HttpRequest, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if not request.user.following.filter(id=user_id).exists():
        Follow.objects.create(follower=request.user, following=user_to_follow)
    return redirect('profile_detail', pk=user_to_follow.id)

@login_required
def unfollow_user(request: HttpRequest, user_id):
    Follow.objects.filter(following_id=user_id).delete()
    return redirect('profile_detail', pk=user_id)


@login_required
@transaction.atomic
def profile(request: HttpRequest):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    },
    )


@login_required
@transaction.atomic
def update_profile(request: HttpRequest):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Ваш профиль успешно обновлён!'))
            return redirect('my_profile')
        else:
            messages.error(request, ('Пожалуйста, исправьте ошибку!'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


def profile_detail(request: HttpRequest, pk):
    user_obj: User = get_object_or_404(User, pk=pk)
    is_follow = False
    current_user: User = request.user
    following_users = User.objects.followed_by_user(user_obj.id)
    follower_users = User.objects.follows_user(user_obj.id)

    if current_user.following.filter(following_id=pk).exists():
        is_follow = True

    return render (request, 'profile_detail.html', {
        "user_obj": user_obj,
        "is_follow": is_follow,
        "following_users": following_users,
        "follower_users": follower_users,
    }
)
