from django.db import models
from django import forms
from django.contrib.auth.models import User, Group

# # Allow multiple Groups with the same name
# Group._meta.get_field('name')._unique = False

class UserProfile(models.Model):
	# Django documentation for built-in User model:
	#	https://docs.djangoproject.com/en/1.7/ref/contrib/auth/#django.contrib.auth.models.User
    
	# This line is required. Links UserProfile to a User model instance.
	user = models.OneToOneField(User)

	# The additional attributes we wish to include.
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)

	# Override the __unicode__() method to return out something meaningful!
	def __unicode__(self):
		return self.user.username

	class Meta:
		permissions = (
			('site_manager', 'Has site manager privileges'),
		)

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'password', 'first_name', 'last_name', 'email')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')