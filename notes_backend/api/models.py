from django.db import models
from django.contrib.auth.models import User

# PUBLIC_INTERFACE
class Note(models.Model):
    """
    Represents a note created by a user.
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')

    def __str__(self):
        return f"{self.title} ({self.user.username})"
