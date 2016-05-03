from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group, Permission
from users.models import UserForm, EditUserForm, UserProfile, UserProfileForm
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from social.backends.utils import load_backends
from django.conf import settings
from django.template.loader import render_to_string
from django.db.models import Q
import safecollab

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

			return HttpResponseRedirect('/home')

		# Invalid form or forms - mistakes or something else?
		# Print problems to the terminal.
		# They'll also be shown to the user.
		else:
			context_dict = {
				'user_form': user_form,
				'profile_form': profile_form,
			}
			return render(request, 'index.html', context_dict)

	# Not a HTTP POST, this should never happen
	else:
		context_dict = {
			'user_form': UserForm(),
			'profile_form': UserProfileForm(),
			'error_messages': ['Invalid HTTP request.']
		}
		return render(request,'index.html',context_dict)

def register_social(request):
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

			user.backend = 'django.contrib.auth.backends.ModelBackend'
			login(request, user)

			backend = request.session['partial_pipeline']['backend']
			return redirect('social:complete', backend=backend)

		# Invalid form or forms - mistakes or something else?
		# Print problems to the terminal.
		# They'll also be shown to the user.
		else:
			print(user_form.errors, profile_form.errors)

			context_dict = {
				'user_form': user_form,
				'profile_form': profile_form,
				'backend': request.session['partial_pipeline']['backend'],
			}

			return render(request, 'register_social.html', context_dict)

	else:
		partial_user_data = request.session.get('partial_user_data')

		context_dict = {
			'user_form': UserForm(initial=partial_user_data),
			'profile_form': UserProfileForm(),
			'backend': request.session['partial_pipeline']['backend'],
		}

		request.session.pop('partial_user_data')

		return render(request, 'register_social.html', context_dict)

def associate_social(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				backend = request.session['partial_pipeline']['backend']
				return redirect('social:complete', backend=backend)
			else:
				# An inactive account was used...
				context_dict = {
					'user_form': UserForm(),
					'profile_form': UserProfileForm(),
					'error_messages': ['Inactive account used. Social auth association failed.']
				}
				return render(request,'index.html',context_dict)
		else:
			# Bad login credentials.
			context_dict = {
				'user_form': UserForm(),
				'profile_form': UserProfileForm(),
				'error_messages': ['Invalid login details supplied. Social auth association failed.']
			}
			return render(request,'index.html',context_dict)
	else:
		# This should not happen.
		context_dict = {
			'user_form': UserForm(),
			'profile_form': UserProfileForm(),
			'error_messages': ['An error occurred during social auth association.']
		}
		return render(request,'index.html',context_dict)

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
				context_dict = {
					'user_form': UserForm(),
					'profile_form': UserProfileForm(),
					'error_messages': ['Your SafeCollab account has been disabled.']
				}
				return render(request,'index.html',context_dict)
		else:
			# Bad login details were provided. So we can't log the user in.
			context_dict = {
				'user_form': UserForm(),
				'profile_form': UserProfileForm(),
				'error_messages': ['Invalid login details supplied.']
			}
			return render(request,'index.html',context_dict)

	# Not a HTTP POST, this should never happen
	else:
		context_dict = {
			'user_form': UserForm(),
			'profile_form': UserProfileForm(),
			'error_messages': ['Invalid HTTP request.']
		}
		return render(request,'index.html',context_dict)


@csrf_exempt
def fda_login(request):
	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		#print("TEST")
		if user:
			if user.is_active:
				# If the account is valid and active, we can log the user in.
				# We'll send the user back to the homepage.
				print("Login succeeded")
				login(request, user)
				return HttpResponse("success")
			else:
				# An inactive account was used - no logging in!
				print("Login Failed")
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
	return HttpResponseRedirect('/')

@login_required
def grant_sm(request, user_id):
	# try to find user
	query_set = User.objects.filter(id=int(user_id))
	if query_set.exists():
		user = query_set[0]
		permission = Permission.objects.get(codename='site_manager')
		if permission in user.user_permissions.all():

			return HttpResponse('User %s is already a site manager'%(user.username))
		user.user_permissions.add(permission)
		return HttpResponseRedirect('/users/'+str(user_id)+'/')
	else:

		return HttpResponse('User not found.')

@login_required
def revoke_sm(request, user_id):
	# try to find user
	query_set = User.objects.filter(id=int(user_id))
	if query_set.exists():
		user = query_set[0]
		permission = Permission.objects.get(codename='site_manager')
		if not permission in user.user_permissions.all():
			return HttpResponse('User %s is already not a site manager'%(user.username))
		user.user_permissions.remove(permission)
		return HttpResponseRedirect('/users/'+str(user_id)+'/')
	else:
		return HttpResponse('User not found.')

@login_required
def suspend_user(request, user_id):
	# try to find user
	query_set = User.objects.filter(id=int(user_id))
	if query_set.exists():
		user = query_set[0]
		if user.is_active:
			user.is_active = False
			# Update user object in database
			user.save()
		return HttpResponseRedirect('/users/'+str(user_id)+'/')
		return HttpResponse('User %s is already suspended'%(user.username))
	else:
		return HttpResponse('User not found.')

@login_required
def restore_user(request, user_id):
	# try to find user
	query_set = User.objects.filter(id=int(user_id))
	if query_set.exists():
		user = query_set[0]
		if not user.is_active:
			user.is_active = True
			# Update user object in database
			user.save()
		return HttpResponseRedirect('/users/'+str(user_id)+'/')
		return HttpResponse('User %s is already active'%(user.username))
	else:
		return HttpResponse('User not found.')



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
			error_messages = ['Group under name "' + group_name + '" already exists. Click <a href="/groups/' + str(new_group.id) + '/">here</a> for group summary.']
			safecollab.views.groups(request, error_messages=error_messages)

		current_user.groups.add(new_group)
		
		return HttpResponseRedirect('/groups/'+str(new_group.id)+'/')
	return HttpResponse('Inappropriate arrival at /create-group/')

@login_required
def add_user_to_group(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		group_id = request.POST.get('group_id')
		
		query_set = Group.objects.filter(id=int(group_id))
		if not query_set.exists():
			error_messages = ['Group not found.']
			return safecollab.views.groups(request, error_messages=error_messages)
		group = query_set[0]

		# check if current user has permission to add users to group
		if request.user.has_perm('users.site_manager') or request.user.groups.filter(id=int(group_id)).exists():
			query_set = User.objects.filter(username=username)
			if not query_set.exists():
				error_messages = ['User not found.']
				return safecollab.views.group_summary(request, int(group_id), error_messages=error_messages)

			user = query_set[0]
			user.groups.add(group)

			return HttpResponseRedirect('/groups/' + group_id + '/')
		else:
			error_messages = ['You do not have permission to add users to this group.']
			return safecollab.views.group(request, int(group_id), error_messages=error_messages)

	return HttpResponse('Inappropriate arrival at /add-user-to-group/')

@login_required
def remove_user_from_group(request, group_id, user_id):
	# try to find user
	query_set = User.objects.filter(id=int(user_id))
	if query_set.exists():
		user = query_set[0]
		# try to find group
		query_set = user.groups.filter(id=int(group_id))
		if query_set.exists():
			group = query_set[0]
			# remove user from group
			group.user_set.remove(user)
			# delete group if empty
			if not group.user_set.all().exists():
				group.delete()
			# removed by user
			if user_id == request.user.id:
				return HttpResponseRedirect('/groups/')
			# removed by SM
			else:
				return HttpResponseRedirect('/groups/'+str(group_id)+'/')
		else:
			error_messages = ['Group not found.']
			return safecollab.views.groups(request, error_messages=error_messages)
	else:
		error_messages = ['User not found.']
		return safecollab.views.group_summary(request, int(group_id), error_messages=error_messages)

@login_required
def favorite_group(request):
	if request.is_ajax() and request.method == 'POST':
		group_id = request.POST.get('group_id')
		group = Group.objects.get(id=group_id)

		user = request.user
		profile = UserProfile.objects.get(user=user)

		profile.favorite_groups.add(group)

		context_dict = {
			'favorite_groups': profile.favorite_groups.all(),
		}
		html = render_to_string('favorite-groups-table.html', context_dict),
		return HttpResponse(html)

	else:
		# This should never happen
		return HttpResponse('Improper arrival at favorite_group, see users.views')

@login_required
def unfavorite_group(request):
	if request.is_ajax() and request.method == 'POST':
		group_id = request.POST.get('group_id')
		group = Group.objects.get(id=group_id)

		user = request.user
		profile = UserProfile.objects.get(user=user)
		
		profile.favorite_groups.remove(group)

		context_dict = {
			'favorite_groups': profile.favorite_groups.all(),
		}
		html = render_to_string('favorite-groups-table.html', context_dict),
		return HttpResponse(html)

	else:
		# This should never happen
		return HttpResponse('Improper arrival at unfavorite_group, see users.views')



###############################
#####                     #####
#####       Settings      #####
#####                     #####
###############################

@login_required
def view_profile(request, user_id, **kwargs):
	query_set = User.objects.filter(id=user_id)
	if not query_set.exists():
		return view_profile(request, request.user.id, error_messages=['User with user_id='+str(user_id)+' could not be found.'])
	user = query_set[0]

	profile = None
	query_set = UserProfile.objects.filter(user=user)
	if not query_set.exists():
		profile = UserProfile()
		profile.user = user
		profile.save()
	else:
		profile = query_set[0]

	context_dict = {}

	if int(user_id) == int(request.user.id):
		context_dict = {
			'user_form': EditUserForm(initial=model_to_dict(user)),
			'profile_form': UserProfileForm(initial=model_to_dict(profile)),
			'available_backends': load_backends(settings.AUTHENTICATION_BACKENDS),
			'editing': 'editing' in kwargs and kwargs['editing'] == 'editing',
		}
	context_dict['disp_user'] = user
	context_dict['disp_user_is_sm'] = (user.is_superuser) or (Permission.objects.get(codename='site_manager') in user.user_permissions.all()) #user.has_perm('users.site_manager')

	if 'error_messages' in kwargs:
		context_dict['error_messages'] = kwargs['error_messages']

	return render(request, 'profile.html', context_dict)

@login_required
def edit_profile(request):
	# If it's a HTTP POST, we're interested in processing form data.
	if request.method == 'POST':
		# Attempt to grab information from the raw form information.
		# Note that we make use of both UserForm and UserProfileForm.

		user = request.user
		profile = None
		query_set = UserProfile.objects.filter(user=user)
		if not query_set.exists():
			profile = UserProfile()
			profile.user = user
			profile.save()
		else:
			profile = query_set[0]


		if 'username' in request.POST and request.POST.get('username'):
			if User.objects.filter(username=str(request.POST.get('username'))).exists():
				error_messages = ['Username "' + str(request.POST.get('username')) + '" is already taken.']
				return view_profile(request, request.user.id, error_messages=error_messages)
			user.username = request.POST.get('username')
		if 'password' in request.POST and request.POST.get('password'):
			user.set_password(request.POST.get('password'))
		if 'first_name' in request.POST and request.POST.get('first_name'):
			user.first_name = request.POST.get('first_name')
		if 'last_name' in request.POST and request.POST.get('last_name'):
			user.last_name = request.POST.get('last_name')
		if 'email' in request.POST and request.POST.get('email'):
			user.email = request.POST.get('email')
		user.save()

		if 'picture-clear' in request.POST:
			profile.picture.delete(save=False)
		elif 'picture' in request.FILES:
			profile.picture = request.FILES['picture']
		if 'website' in request.POST and request.POST.get('website'):
			profile.website = request.POST.get('website')
		profile.save()
		
		return HttpResponseRedirect('/users/'+str(user.id))

	# Not a HTTP POST, this should never happen
	else:
		return view_profile(request, request.user.id, error_messages=['An error occurred while editing profile.'])

