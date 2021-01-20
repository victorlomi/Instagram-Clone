from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Image(models.Model):
	image = models.ImageField(upload_to="photos/")
	name = models.CharField(max_length=60)
	description = models.TextField()
	Profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

	def __str__(self):
		return self.name
