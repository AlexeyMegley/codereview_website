from django.db import models
from skills.models import Skill
from github_api.github_api_helpers import FILE_EXTENSIONS
from .exceptions import LanguageValidationError


class GithubProjectManager(models.Manager):

    def create_project(self, language, url, last_commit):
        if language and language.lower() in FILE_EXTENSIONS:
            skill, _ = Skill.objects.get_or_create(name=language.lower())
            project = self.model(skill=skill, url=url, last_commit=last_commit)
            project.save(force_insert=True)
            return project
        raise LanguageValidationError('Project language has no support')

