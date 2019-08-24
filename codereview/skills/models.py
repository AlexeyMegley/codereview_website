from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)
    level = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)])


class GithubProject(models.Model):
	skill = models.ManyToManyField(Skill, related_name='performed_projects')
	url = models.SlugField(unique=True)
