from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import Programmer
from projects.models import GithubProject


class CodeFile(models.Model):
	github_url = models.URLField(max_length=255, unique=True)
    author = models.ForeignKey(Programmer, on_delete=models.CASCADE)
    project = models.ForeignKey(GithubProject, on_delete=models.CASCADE)
    rating = models.FloatField(validators=[MaxValueValidator(10), MinValueValidator(1)])
    text = models.TextField()


class Review(models.Model):
    date_creation = models.DateField(auto_now_add=True)
    code_file = models.ForeignKey(CodeFile, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(Programmer, on_delete=models.CASCADE)
    mark = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)])
    comment = models.TextField()


