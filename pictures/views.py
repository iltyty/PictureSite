from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .forms import UploadForm
from .models import Post


def index(request):
    return render(request, "index.html")


class UploadHistoryView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "process.html"

    def get_queryset(self):
        queryset = Post.objects.all()
        return queryset.filter(user=self.request.user)


class UploadImageView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = UploadForm
    template_name = "upload.html"
    success_url = reverse_lazy("upload_history")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditImageView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "detail.html"
    context_object_name = "obj"


class DeleteImageView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "delete.html"
    success_url = reverse_lazy("upload_history")

    def post(self, request, *args, **kwargs):
        try:
            pk = self.request.POST["pk"]
            Post.objects.filter(pk=pk).delete()
            return JsonResponse({"result": True})
        except Exception as e:
            return super().post(request, *args, **kwargs)