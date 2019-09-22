import asyncio
import defaultdict

from django import timezone
from django.core.exceptions import ObjectDoesNotExist

from users.models import Programmer
from projects.models import GithubProject
from skills.models import Skill

from projects.managers import GithubProjectManager
from github_api.github_api_helpers import get_users_projects


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


def renew_projects_information():
	# Get all users and all their data...
	programmers = Programmer.objects.selected_related('github_projects', 'skills').all()
	
	# For every user get all projects and skills
	github_urls = [p['github_account'] for p in programmers]
    users_projects = loop.run_until_complete(get_users_projects(github_urls))
    
    user_projects_to_create = defaultdict(list)
    projects_to_update = []
    new_skills = []

    for programmer in programmers:
    	projects = users_projects.get(programmer['github_account']) or []
    	for project in projects:
    		try:
    		    project_in_db = programmer.github_projects.get(url=project['url'])
    		except ObjectDoesNotExist:
    			user_projects_to_create[programmer['pk']].append(project)
    			new_user_skills.append(project['language'])
    		else:
    			# Check if project has been updated recently
    			if project_in_db['last_commit'] < project['updated_at']:
    				projects_to_update.append(project)
    
    # Bulk create skills...
    Skill.objects.bulk_create([Skill(name=skill_name) for skill_name in new_skills], ignore_conflicts=True)

    # Bulk create projects...
    language_to_skill = {}
    for skill_obj in Skill.objects.filter(name__in=new_skills):
    	language_to_skill[skill_obj['name']] = skill_obj

	GithubProjectManager.bulk_create(
		[GithubProject(skill=language_to_skill.get(project['language']),
		               url=project['url'], 
		               last_commit=project['updated_at'])
		for user_projects in user_projects_to_create.values()
		for project in user_projects_to_create
	])

	# Bulk update projects...
	urls_to_update = {project['url']: project['updated_at'] for project in projects_to_update}
	projects_to_update_qs = GithubProjectManager.filter(url__in=urls_to_update)
	for project in projects_to_update_qs:
		project['last_commit'] = urls_to_update[project['url']]

	GithubProjectManager.bulk_update(projects_to_update_qs, ['last_commit'])



def fill_reviews_queue(projects):
	# ASYNCHRONOUS Get for every project changed files...
	# Add new reviews (bulk_create)
	pass

def start_indexation():
    renew_projects_information()
    fill_reviews_queue([])
    # Add last_indexation_date (bulk_update)
	pass


def start_indexation_in_bg():
    pass

