from django.db import models

# Create your models here.

# Rating will be count by the next formula:
# Common_Rating = 10 - 4 * (1/(project_rating + 1)) - 3 * (1/(skill_startdate + 1)) - 2 * (1/(first_commit + 1))
