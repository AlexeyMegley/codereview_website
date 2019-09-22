import asyncio
from collections import defaultdict
from time import time

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from users.models import Programmer
from projects.models import GithubProject
from skills.models import Skill
from .models import Indexation
from projects.managers import GithubProjectManager
from github_api.github_api_helpers import get_users_projects


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


def renew_projects_info():
    # Get all users and all their data...
    programmers = Programmer.objects.select_related().all()
    
    # For every user get all projects and skills
    github_urls = [p.github_account for p in programmers]
    fetched_project_data = loop.run_until_complete(get_users_projects(github_urls))

    # Merge all data in the single dict
    user_to_projects = {}
    for user_projects in fetched_project_data:
        user_to_projects.update(user_projects)

    user_projects_to_create = defaultdict(list)
    projects_to_update = []
    new_skills = []

    for programmer in programmers:

        projects = user_to_projects.get(programmer.github_account) or []
        for project in projects:

            # Check if project should be added
            if not GithubProjectManager.lang_is_supported(project['language']): 
                continue

            try:
                project_in_db = programmer.github_projects.get(url=project['url'])
            except ObjectDoesNotExist:
                user_projects_to_create[programmer.pk].append(project)
                new_skills.append(project['language'])
            else:
                # Check if project has been updated recently
                if project_in_db.last_commit < project['updated_at']:
                    projects_to_update.append(project)

                    # maybe new commits made a difference
                    new_skills.append(project['language'])

    # Bulk create skills...
    Skill.objects.bulk_create([Skill(name=skill_name) for skill_name in new_skills], ignore_conflicts=True)

    # Bulk create projects...
    if user_projects_to_create:
        language_to_skill = {}
        for skill_obj in Skill.objects.filter(name__in=new_skills):
            language_to_skill[skill_obj.name] = skill_obj

        GithubProject.objects.bulk_create(
            [GithubProject(skill=language_to_skill.get(project['language']),
                           url=project['url'], 
                           last_commit=project['updated_at'])
            for user_projects in user_projects_to_create.values()
            for project in user_projects
            ]
        )
    
    # Bulk update projects...
    if projects_to_update:
        urls_to_update = {project['url']: project['updated_at'] for project in projects_to_update}
        projects_to_update_qs = GithubProject.objects.filter(url__in=urls_to_update)
        for project in projects_to_update_qs:
            project.last_commit = urls_to_update[project.url]

        GithubProject.objects.bulk_update(projects_to_update_qs, ['last_commit'])


def fill_reviews_queue(projects):
    # ASYNCHRONOUS Get for every project changed files...
    # Add new reviews (bulk_create)
    pass

def start_indexation():
    
    start_indexation = time()
    indexation = Indexation.load()
    renew_projects_info()
    
    # Get projects where last commit is later than last successfull indexation
    projects = GithubProject.objects.filter(last_commit__gt=indexation.last_successfull_indexation)
    fill_reviews_queue([project.url for project in projects])

    # Add last_indexation_date (bulk_update)
    end_indexation = time()
    indexation = Indexation.load()
    indexation.last_successfull_indexation = timezone.now().date()
    indexation.duration_in_seconds = round(end_indexation - start_indexation)
    indexation.save()


def start_indexation_in_bg():
    pass

