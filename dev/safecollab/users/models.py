from django.db import models
from django import forms

class User(models.Model):
    first_name = models.CharField(max_length=30)		# First name
    last_name = models.CharField(max_length=30)			# Last name
    user_id = models.CharField(max_length=30)			# User ID
    password = models.CharField(max_length=30)			# Password
    site_manager = models.BooleanField(default=False)	# Site-manager field

class RegisterForm(forms.Form):
	class Meta:
		model = User
		first_name = forms.CharField(max_length=30)
		password = forms.PasswordInput()
		fields = ['first_name','last_name','user_id','password']
		widgets = {
			'password': forms.PasswordInput(),
		}

class LoginForm(forms.Form):
    class Meta:
        model = User
        fields = ['user_id','password']
        widgets = {
            'password': forms.PasswordInput(),
        }