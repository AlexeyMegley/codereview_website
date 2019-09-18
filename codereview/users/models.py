import threading
from datetime import date

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver

from .managers import ProgrammerManager
from skills.models import Skill, SkillRating
from projects.models import GithubProject
from projects.exceptions import LanguageValidationError
from snippets.models import Snippet
from github_api.github_api_helpers import fetch_user_repo_data


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

    
    def get_short_name(self):
        return self.github_account

    def get_full_name(self):
        return self.get_short_name()

    def fill_github_data(self):
        user_projects = fetch_user_repo_data(self.github_account)
        first_commit = date.today()
        for project in user_projects:
            language = project['language']
            project_url = project['url']
            last_project_commit = project['updated_at']
            first_commit = min(first_commit, project['created_at'])
            try:
                project = GithubProject.objects.create_project(language, project_url, last_project_commit)
                self.github_projects.add(project)
            except LanguageValidationError:
                # TODO Log will be here soon...
                print(f"'{language}' is not supported. Maybe add support for it?")

        self.first_commit = first_commit
        self.save()

    def sync_github_data(self):
        pass

    def sync_github_data_in_bg(self):
        """ Fetch user data from github and sync it with data in the database """
        t = threading.Thread(target=self.sync_github_data, args=(), kwargs={})
        t.setDaemon(True)
        t.start()


class UserSettings(models.Model):
    user = models.OneToOneField(Programmer, on_delete=models.CASCADE)
    review_code_from_date = models.DateField()
    review_skills = models.ManyToManyField(Skill)
    review_projects = models.ManyToManyField(GithubProject)


@receiver(post_save, sender=Programmer, dispatch_uid='fill_github_data_in_bg_count')
def fill_github_data_in_bg(sender, instance, **kwargs):
    # Start operation on new users or users, which still have no projects on github
    # TODO - use Celery later
    if not instance.github_projects.exists():
        t = threading.Thread(name="bg_thread", target=instance.fill_github_data, args=(), kwargs={})
        t.setDaemon(True)
        t.start()