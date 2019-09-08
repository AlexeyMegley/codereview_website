from django.contrib.auth.models import BaseUserManager


class ProgrammerManager(BaseUserManager):
	use_in_migrations = True

	def create_user(self, github_account, email=None, username=None, password=None):
		if not github_account:
			raise ValueError("Github account is required!")

		user = self.model(github_account=github_account)
		user.save()
		return user

	def create_superuser(self, github_account, email=None, username=None, password=None):
		user = self.create_user(github_account)
		user.is_staff = True
		user.is_superuser = True
		user.save()
		return user
