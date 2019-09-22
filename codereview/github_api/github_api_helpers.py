import requests
import asyncio
import aiohttp
from datetime import datetime

from django.conf import settings


BASE_API_URL = 'https://api.github.com'
CLIENT_ID = settings.SOCIAL_AUTH_GITHUB_KEY
CLIENT_SECRET = settings.SOCIAL_AUTH_GITHUB_SECRET
COMMITS_TO_FETCH = 100
DATETIME_GITHUB_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
FILE_EXTENSIONS = {
    'python': 'py',
    'c': 'c',
    'c++': 'cpp',
    'c#': 'cs',
    'java': 'java',
    'go': 'go',
    'javascript': 'js',
    'typescript': 'ts',
    'objective-c': 'm',
    'coffeescript': 'coffee',
    'swift': 'swift',
    'assembly': 'asm',
    'perl': 'pl',
    'd': 'd',
    'f#': 'fs',
    'kotlin': 'kt',
    'julia': 'jl',
    'ruby': 'rb',
    'elixir': 'ex',
    'crystal': 'cr',
    'clojure': 'clj',
    'scala': 'scala',
    'scheme': 'scm',
    'erlang': 'erl',
    'webassembly': 'wast',
    'haskell': 'hs',
    'ocalm': 'ml',
    'rust': 'rs',
    'php': 'php',
    'visual basic': 'vb',
    'r': 'r',
    'lua': 'lua',
    'lisp': 'lisp',
}


def get_necessary_data(raw_data: [dict]) -> [dict]:
    return [
                {
                  'created_at': datetime.strptime(project['created_at'], DATETIME_GITHUB_FORMAT).date(), 
                  'updated_at': datetime.strptime(project['updated_at'], DATETIME_GITHUB_FORMAT).date(),
                  'language': project['language'],
                  'url': project['url']
                } 
                for project in raw_data
            ]


def fetch_user_repo_data(github_username: str) -> {str: [dict]}:
    url = f'{BASE_API_URL}/users/{github_username}/repos'
    raw_data = requests.get(url, data={'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET}).json()
    return get_necessary_data(raw_data)


async def fetch_user_repo_data_async(github_username: str, session: aiohttp.ClientSession) -> [dict]:
    url = f'{BASE_API_URL}/users/{github_username}/repos'
    resp = await session.request(method="GET", url=url, headers={'client_id': CLIENT_ID,
                                                                 'client_secret': CLIENT_SECRET})
    resp.raise_for_status()
    raw_data = await resp.json()
    return {github_username: get_necessary_data(raw_data)}


async def get_users_projects(github_usernames: [str]) -> [{str: [dict]}]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_user_repo_data_async(account, session)
                 for account in github_usernames]
        return await asyncio.gather(*tasks)
