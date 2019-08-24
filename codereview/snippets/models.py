from django.db import models

from skills.models import Skill

class Snippet(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey('users.Programmer', on_delete=models.CASCADE)
