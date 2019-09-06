from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=200)
    cover = models.ImageField(upload_to="images/")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    # def save(self, *args, **kwargs):
    #     if not self.created:
    #         self.created = timezone.now()

    #     self.updated = timezone.now()
    #     return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
