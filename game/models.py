from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    # Remove first_name, last_name, email fields by overriding with None
    first_name = None
    last_name = None
    email = None

class AStarPath(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_row = models.IntegerField()
    start_col = models.IntegerField()
    goal_row = models.IntegerField()
    goal_col = models.IntegerField()
    path = models.TextField()
    path_length = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"A* ({self.start_row},{self.start_col}) → ({self.goal_row},{self.goal_col})"

class DijkstraPath(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_row = models.IntegerField()
    start_col = models.IntegerField()
    goal_row = models.IntegerField()
    goal_col = models.IntegerField()
    path = models.TextField()
    path_length = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dijkstra ({self.start_row},{self.start_col}) → ({self.goal_row},{self.goal_col})"
