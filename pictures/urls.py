from django.urls import path
from . import views
from .views import UploadImageView, UploadHistoryView, EditImageView


urlpatterns = [
    path("", views.index, name="pictures_index"),
    path("upload/", UploadImageView.as_view(), name="upload_image"),
    path("process/", UploadHistoryView.as_view(), name="upload_history"),
    path("process/detail/<pk>/", EditImageView.as_view(), name="detail"),
]
