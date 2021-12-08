from django.db import models
from django.db.models.base import Model
from django.contrib.auth import get_user_model
from django.urls import reverse

class Book(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    publisher = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('book_detail', args=[self.id])