from django.db import models
from skills.models import Skill
from .managers import GithubProjectManager


class GithubProject(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, default=None)
    url = models.URLField(unique=True, max_length=255)
    last_commit = models.DateField()
    
    objects = GithubProjectManager()