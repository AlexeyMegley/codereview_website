from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from .managers import ProgrammerManager
from skills.models import Skill, SkillRating, GithubProject
from snippets.models import Snippet


class Programmer(AbstractBaseUser, PermissionsMixin):
    github_account  = models.URLField(max_length=255, unique=True)
    skills = models.ManyToManyField(SkillRating, related_name='competent_users')
    date_creation = models.DateField(auto_now_add=True)
    github_projects = models.ManyToManyField(GithubProject, related_name='committers')
    snippets = models.ManyToManyField(Snippet, related_name='users_added')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_indexation_date = models.DateField(auto_now_add=True)
    first_commit = models.DateField(auto_now_add=True)

    objects = ProgrammerManager()

    USERNAME_FIELD = 'github_account'
    REQUIRED_FIELDS = []

    class Meta:
    	verbose_name = 'programmer'
    	verbose_name_plural = 'programmers'

    def get_full_name(self):
    	return 'Full Name'

    def get_short_name(self):
    	return 'Short Name'

    def update_user_skills(self):
    	""" Necessary data will be taken from github_account """
    	return


class UserSettings(models.Model):
    user = models.OneToOneField(Programmer, on_delete=models.CASCADE)
    review_code_from_date = models.DateField()
    review_skills = models.ManyToManyField(Skill)
    review_projects = models.ManyToManyField(GithubProject)

