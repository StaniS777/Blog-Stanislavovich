import datetime
import time
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    CreateView,
    DetailView, 
    ListView,
)
from django.template.loader import render_to_string
from publication.forms import PublicUpdateCreateForm
from publication.models import Public


class PublicDetailView(DetailView):
    template_name = "public_detail.html"
    model = Public
    
    queryset = Public.objects.select_related("author")


class PublicListView(ListView):
    model = Public
    template_name = "public_list.html"
    queryset = Public.objects.order_by("-created")
    paginate_by = 10


class AddLike(LoginRequiredMixin, View):
    @csrf_exempt
    def post(self, request, pk, *args, **kwargs):
        post = Public.objects.get(pk=pk)

        is_dislike = False

        for dislike in post.dislikes.all():

            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = request.user in post.likes.all()

        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)
        
        return JsonResponse({"status": "ok",
                             "like_count":post.likes.count(),
                             "dislike_count":post.dislikes.count()})



class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Public.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user)

        is_dislike = request.user in post.dislikes.all()

        if not is_dislike:
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)

        return JsonResponse({"status": "ok",
                             "like_count":post.likes.count(),
                             "dislike_count":post.dislikes.count()})
    

class MyPublicListView(LoginRequiredMixin, ListView):
    template_name = "public_mine.html"
    model = Public
    queryset = Public.objects.order_by("-created")

    def get_queryset(self) -> QuerySet[Public]:
        queryset = super().get_queryset()
        queryset = queryset.filter(author=self.request.user)
        return queryset
    

class PublicCreateView(LoginRequiredMixin, CreateView):
    template_name = "public_create.html"
    model = Public
    form_class = PublicUpdateCreateForm
    success_url = reverse_lazy("public_list")

    def form_valid(self, form: PublicUpdateCreateForm) -> HttpResponse:
        self.object: Public = form.save(commit=False)
        self.object.author = self.request.user
        self.object.created = datetime.datetime.now()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())