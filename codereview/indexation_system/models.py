from datetime.utils import timezone

from django.db import models


class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Indexation(SingletonModel):
    
    last_successfull_indexation = models.DateField(default=timezone.now().date())
    duration_in_seconds = models.IntegerField(default=0)
