from django.db import models
from skills.models import Skill
from github_api.github_api_helpers import FILE_EXTENSIONS
from .exceptions import LanguageValidationError


class GithubProjectManager(models.Manager):

    def create_project(self, language, url, last_commit):
        if self.lang_is_supported(language):
            skill, _ = Skill.objects.get_or_create(name=language.lower())
            project = self.model(skill=skill, url=url, last_commit=last_commit)
            project.save()
            return project
        raise LanguageValidationError('Project language has no support')
    
    @classmethod
    def lang_is_supported(cls, language):
        return language and language.lower() in FILE_EXTENSIONS

