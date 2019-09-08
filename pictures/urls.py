from django.urls import path
from . import views
from .views import (
    UploadImageView,
    UserUploadHistoryView,
    AdminUploadHistoryView,
    UserSpecifiedHistoryView,
    EditImageView,
    DeleteImageView,
    DeleteImagesView,
)


urlpatterns = [
    path("", views.index, name="pictures_index"),
    path("upload/", UploadImageView.as_view(), name="upload_image"),
    path(
        "process/history/user/<username>/",
        UserUploadHistoryView.as_view(),
        name="upload_history_user",
    ),
    path(
        "process/history/admin/<adminname>/",
        AdminUploadHistoryView.as_view(),
        name="upload_history_admin",
    ),
    path(
        "process/history/admin/<adminname>/specified/",
        UserSpecifiedHistoryView.as_view(),
        name="upload_history_specified",
    ),
    path("process/detail/<pk>/", EditImageView.as_view(), name="detail"),
    path("process/delete/<pk>/", DeleteImageView.as_view(), name="delete_image"),
    path("process/deletes/", DeleteImagesView.as_view(), name="delete_images"),
]
