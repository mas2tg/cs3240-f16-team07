from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group, Permission
from users.models import UserForm, UserProfile, UserProfileForm

###############################
#####                     #####
#####   Authentication    #####
#####                     #####
###############################

def register(request):
	# Redirect user if already logged in.
	if request.user:
		if request.user.is_authenticated():
			return HttpResponseRedirect('/home')

	# A boolean value for telling the template whether the registration was successful.
	# Set to False initially. Code changes value to True when registration succeeds.
	registered = False

	# If it's a HTTP POST, we're interested in processing form data.
	if request.method == 'POST':
		# Attempt to grab information from the raw form information.
		# Note that we make use of both UserForm and UserProfileForm.
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		# If the two forms are valid...
		if user_form.is_valid() and profile_form.is_valid():
			# Save the user's form data to the database.
			user = user_form.save()

			# Now we hash the password with the set_password method.
			# Once hashed, we can update the user object.
			user.set_password(user.password)
			user.save()

			# Now sort out the UserProfile instance.
			# Since we need to set the user attribute ourselves, we set commit=False.
			# This delays saving the model until we're ready to avoid integrity problems.
			profile = profile_form.save(commit=False)
			profile.user = user

			# Did the user provide a profile picture?
			# If so, we need to get it from the input form and put it in the UserProfile model.
			if 'picture' in request.FILES:
				 profile.picture = request.FILES['picture']

			# Now we save the UserProfile model instance.
			profile.save()

			# Update our variable to tell the template registration was successful.
			registered = True
			return HttpResponseRedirect('/home')

		# Invalid form or forms - mistakes or something else?
		# Print problems to the terminal.
		# They'll also be shown to the user.
		else:
			print(user_form.errors, profile_form.errors)
			return HttpResponse('Errors with form')

	# Not a HTTP POST, this should never happen
	else:
		return HttpResponse('Error in register() see users.views')

def user_login(request):
	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
	# Gather the username and password provided by the user.
		# This information is obtained from the login form.
				# We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
				# because the request.POST.get('<variable>') returns None, if the value does not exist,
				# while the request.POST['<variable>'] will raise key error exception
		username = request.POST.get('username')
		password = request.POST.get('password')

		# Use Django's machinery to attempt to see if the username/password
		# combination is valid - a User object is returned if it is.
		user = authenticate(username=username, password=password)

		# If we have a User object, the details are correct.
		# If None (Python's way of representing the absence of a value), no user
		# with matching credentials was found.
		if user:
			# Is the account active? It could have been disabled.
			if user.is_active:
				# If the account is valid and active, we can log the user in.
				# We'll send the user back to the homepage.
				login(request, user)
				return HttpResponseRedirect('/home')
			else:
				# An inactive account was used - no logging in!
				return HttpResponse("Your SafeCollab account is disabled.")
		else:
			# Bad login details were provided. So we can't log the user in.
			print ("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied.")

	# Not a HTTP POST, this should never happen
	else:
		return HttpResponse('Error in user_login() see users.views')

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
	# Since we know the user is logged in, we can now just log them out.
	logout(request)

	 # Take the user back to the homepage.
	return HttpResponseRedirect('/index')

@login_required
def new_site_manager(request):
	if request.method == 'POST':
		if request.user.has_perm('users.site_manager'):
			username = request.POST.get('username')
			user = User.objects.get(username=username)
			permission = Permission.objects.get(codename='site_manager')
			if user.has_perm(permission):
				return HttpResponse('User %s is already a site manager'%(username))
			user.user_permissions.add(permission)
			return HttpResponse('User %s is now a site manager'%(username))

	return HttpResponse('Inappropriate arrival at /new-site-manager/')

@login_required
def suspend_user(request):
	if request.method == 'POST' and request.user.has_perm('users.site_manager'):
		username = request.POST.get('username')
		user = User.objects.get(username=username)
		if user:
			if user.is_active:
				user.is_active = False
				# Update user object in database
				user.save()
				return HttpResponse('User %s is now suspended'%(username))
			return HttpResponse('User %s is already suspended'%(username))
		else:
			return HttpResponse('User %s does not exist'%(username))

	return HttpResponse('Inappropriate arrival at /suspend-user/')

@login_required
def restore_user(request):
	if request.method == 'POST' and request.user.has_perm('users.site_manager'):
		username = request.POST.get('username')
		user = User.objects.get(username=username)
		if not user.is_active:
			user.is_active = True
			# Update user object in database
			user.save()
			return HttpResponse('User %s is now active'%(username))
		return HttpResponse('User %s is already active'%(username))

	return HttpResponse('Inappropriate arrival at /suspend-user/')


###############################
#####                     #####
#####     User groups     #####
#####                     #####
###############################

""" Group stuff since we do not have a groups app at the moment.
	If more functionality is required of gorups in the future and
		a separate app is created, these should be moved there.
		For now though the built-in Django group ManyToMany
		relation seems sufficient. """

@login_required
def create_group(request):
	if request.method == 'POST':
		current_user = request.user
		group_name = request.POST.get('group_name')
		
		""" This stuff is relevant if duplicate group names are not allowed """
		new_group, created = Group.objects.get_or_create(name=group_name)
		if not created:
			# Group already exists under that name
			return HttpResponse('Group under name "' + group_name + '" already exists. Click <a href="/groups?name=' + group_name + '">here</a> for group summary.')

		current_user.groups.add(new_group)
		
		return HttpResponseRedirect('/groups?name='+str(new_group.name))
	return HttpResponse('Inappropriate arrival at /create-group/')

def add_user_to_group(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		group_name = request.POST.get('group_name')
		
		group = Group.objects.get(name=group_name)
		user = User.objects.get(username=username)
		# TODO: add check for whether group/user exists

		user.groups.add(group)

		return HttpResponseRedirect('/groups?name='+group_name)

	return HttpResponse('Inappropriate arrival at /add-user-to-group/')
