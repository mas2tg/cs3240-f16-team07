from django.db import models
from django import forms
from django.contrib.auth.models import User, Group
from inbox.models import Message
from django.core.exceptions import ValidationError

# # Allow multiple Groups with the same name
# Group._meta.get_field('name')._unique = False

def get_received_messages(self):
	return Message.objects.filter(recipient=self)
def get_unread_messages(self):
	return Message.objects.filter(recipient=self, read=False)

User.add_to_class('get_received_messages', get_received_messages)
User.add_to_class('get_unread_messages', get_unread_messages)

class UserProfile(models.Model):
	# Django documentation for built-in User model:
	#	https://docs.djangoproject.com/en/1.7/ref/contrib/auth/#django.contrib.auth.models.User
    
	# This line is required. Links UserProfile to a User model instance.
	# related_name helps with accessing UserProfile when you have corresponding User.
	user = models.OneToOneField(User, related_name='user_profile')

	# The additional attributes we wish to include.
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True, default="")
	favorite_groups = models.ManyToManyField(Group)

	# Override the __unicode__() method to return out something meaningful!
	def __unicode__(self):
		return self.user.username

	class Meta:
		permissions = (
			('site_manager', 'Has site manager privileges'),
		)

class UserForm(forms.ModelForm):
	username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control','required':None}))
	password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control','required':None}))
	first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
	last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
	email = forms.CharField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))

	def clean_username(self):
		username = self.cleaned_data.get('username', '')
		if User.objects.filter(username=username).exists():
			raise ValidationError('Username "' + username + '" taken.")')
		return username
	
	class Meta:
		model = User
		fields = ('username', 'password', 'first_name', 'last_name', 'email')

# username/password fields not required
class EditUserForm(forms.ModelForm):
	username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
	password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
	last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
	email = forms.CharField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))

	def clean_username(self):
		username = self.cleaned_data.get('username', '')
		if User.objects.filter(username=username).exists():
			raise ValidationError('Username "' + username + '" taken.")')
		return username
	
	class Meta:
		model = User
		fields = ('username', 'password', 'first_name', 'last_name', 'email')



class UserProfileForm(forms.ModelForm):
	website = forms.EmailField(required=False, widget=forms.URLInput(attrs={'class': 'form-control'}))
	# Must explicitly say that field is not required in order for ClearableFileInput to render with clear checkbox
	picture = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={}))

	class Meta:
		model = UserProfile
		fields = ('website', 'picture')

class LoginForm(forms.ModelForm):
	username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
	password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	
	class Meta:
		model = User
		fields = ('username', 'password')


