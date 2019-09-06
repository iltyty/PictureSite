from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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
