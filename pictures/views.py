from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView

from .forms import UploadForm
from .models import Post


def index(request):
    return render(request, "index.html")


class UserUploadHistoryView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 9
    template_name = "process_user.html"

    def get_queryset(self):
        queryset = Post.objects.all()

        title = self.request.GET.get("title", "")
        startday = self.request.GET.get("startday", "")
        endday = self.request.GET.get("endday", "")

        if title:
            queryset = queryset.filter(title__contains=title)
        if startday:
            queryset = queryset.filter(created__gte=startday)
        if endday:
            queryset = queryset.filter(created__lte=endday)

        return queryset.filter(user=self.request.user)


class AdminUploadHistoryView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 9
    template_name = "process_admin.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["user_list"] = User.objects.filter(is_superuser=False)
        return data


class UserSpecifiedHistoryView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "process_admin.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["user_list"] = User.objects.filter(is_superuser=False)
        return data

    def get_queryset(self):
        queryset = Post.objects.all()
        user = User.objects.get(username=self.request.GET["user"])
        return queryset.filter(user=user)


class UploadImageView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = UploadForm
    template_name = "upload.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "upload_history_user", kwargs={"username": self.request.user.username}
        )


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


class DeleteImagesView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "delete.html"
    success_url = reverse_lazy("upload_history")

    def post(self, request, *args, **kwargs):
        print("post")
        try:
            ids = self.request.POST.get("ids", "")
            if not ids:
                ids = ids.split(",")
            ids = [int(id) for id in ids]
            Post.objects.filter(pk__in=ids).delete()
            return JsonResponse({"result": True})
        except Exception as e:
            return super().post(request, *args, **kwargs)
