from users.models import *
from projects.models import *
from skills.models import *


def truncate_users():
    Programmer.objects.all().delete()
    GithubProject.objects.all().delete()
    Skill.objects.all().delete()
    print("User data is truncated successfully")
