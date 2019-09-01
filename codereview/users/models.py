from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser
from skills.models import Skill, GithubProject
from snippets.models import Snippet


class Programmer(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    github_account  = models.SlugField(unique=True)
    skills = models.ManyToManyField(Skill, related_name='competent_users')
    rating = models.FloatField(validators=[MaxValueValidator(10), MinValueValidator(1)])
    date_creation = models.DateField(auto_now_add=True)
    first_commit = models.DateField()
    snippets = models.ManyToManyField(Snippet, related_name='users_added')

    USERNAME_FIELD = 'email'


class UserSettings(models.Model):
    user = models.OneToOneField(Programmer, on_delete=models.CASCADE)
    review_code_from_date = models.DateField()
    review_skills = models.ManyToManyField(Skill)
    review_projects = models.ManyToManyField(GithubProject)

