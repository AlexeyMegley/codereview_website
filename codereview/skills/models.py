from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)


class SkillRating(models.Model):
	skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
	rating = models.FloatField(validators=[MaxValueValidator(10), MinValueValidator(1)])

    