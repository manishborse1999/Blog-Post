from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=100)
    views = models.IntegerField(default=0)
    slug = models.CharField(max_length=100)
    timeStamp = models.DateTimeField(default=True)

    def __str__(self):
        return self.title + 'by ' + self.author


class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.comment[0:13] + '.... ' +'by '+ self.user.username