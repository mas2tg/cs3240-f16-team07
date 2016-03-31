from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group, Permission
from users.models import UserForm, UserForm, UserProfileForm

def index(request):
	 context_dict = {
	 	'boldmessage': "I am bold font from the context",
	 }
	 return render(request, 'index.html', context_dict)

def register(request):
	# Redirect user if already logged in.
	if request.user:
		if request.user.is_authenticated():
			return HttpResponseRedirect('/home/')

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

		# Invalid form or forms - mistakes or something else?
		# Print problems to the terminal.
		# They'll also be shown to the user.
		else:
			print(user_form.errors, profile_form.errors)

	# Not a HTTP POST, so we render our form using two ModelForm instances.
	# These forms will be blank, ready for user input.
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	# Render the template depending on the context.
	return render(request,
				'register.html',
				{'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

def user_login(request):
	# Redirect user if already logged in.
	if request.user:
		if request.user.is_authenticated():
			return HttpResponseRedirect('/home/')

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
				return HttpResponseRedirect('/home/')
			else:
				# An inactive account was used - no logging in!
				return HttpResponse("Your SafeCollab account is disabled.")
		else:
			# Bad login details were provided. So we can't log the user in.
			print ("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied.")

	# The request is not a HTTP POST, so display the login form.
	# This scenario would most likely be a HTTP GET.
	else:
		# No context variables to pass to the template system, hence the
		# blank dictionary object...
		return render(request, 'login.html', {})

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
	# Since we know the user is logged in, we can now just log them out.
	logout(request)

	 # Take the user back to the homepage.
	return HttpResponseRedirect('/index/')

def home(request):
	return render(request, 'home.html', {})

@login_required
def create_group(request):
	if request.method == 'POST':
		current_user = request.user
		group_name = request.POST.get('group_name')
		new_group = Group.objects.create(name=group_name)
		
		""" This stuff is srelevant if duplicate group names are not allowed """
		# new_group, created = Group.objects.get_or_create(name=group_name)
		# if not created:
		# 	# Group already exists under that name
		# 	return HttpResponse('Group under name "' + group_name + '" already exists.')

		current_user.groups.add(new_group)
		
		return HttpResponseRedirect('/group-summary?group-id='+str(new_group.id))
	return HttpResponse('Inappropriate arrival at /create-group/')

def group_summary(request):
	if request.method == 'GET':
		group_id = request.GET.get('group-id')
		group = Group.objects.get(id=group_id)
		users = group.user_set.all()

		context_dict = {
			'group': group,
			'users': users,
		}

		return render(request, 'group_summary.html', context_dict)
	return HttpResponse('Inappropriate arrival at /group-summary/')

def add_user_to_group(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		group_id = int(request.POST.get('group_id')) # Must be an int
		
		group = Group.objects.get(id=group_id)
		user = User.objects.get(username=username)
		# TODO: add check for whether group/user exists

		user.groups.add(group)

		return HttpResponseRedirect('/group-summary?group-id='+str(group_id))

	return HttpResponse('Inappropriate arrival at /add-user-to-group/')

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
		if user.is_active:
			user.is_active = False
			return HttpResponse('User %s is now suspended'%(username))
		return HttpResponse('User %s is already suspended'%(username))

	return HttpResponse('Inappropriate arrival at /suspend-user/')

@login_required
def restore_user(request):
	if request.method == 'POST' and request.user.has_perm('users.site_manager'):
		username = request.POST.get('username')
		user = User.objects.get(username=username)
		if not user.is_active:
			user.is_active = True
			return HttpResponse('User %s is now active'%(username))
		return HttpResponse('User %s is already active'%(username))

	return HttpResponse('Inappropriate arrival at /suspend-user/')

# decorator for superuser required
# @user_passes_test(lambda u: u.is_superuser)