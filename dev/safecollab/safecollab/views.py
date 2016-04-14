from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group, Permission
from users.models import UserForm, UserProfileForm
from reports.models import Report, ReportForm
from social.backends.utils import load_backends
from django.conf import settings

def index(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/home')

	context_dict = {
		'user_form': UserForm(),
		'profile_form': UserProfileForm(),
	}
	return render(request, 'index.html', context_dict)

@login_required
def home(request):
	return render(request, 'home.html', {
		'form': ReportForm(),
        'available_backends': load_backends(settings.AUTHENTICATION_BACKENDS)
		})

def groups(request):
	if request.method == 'GET':
		if 'name' in request.GET:
			group_name = request.GET.get('name')
			group = Group.objects.get(name=group_name)
			users = group.user_set.all()

			context_dict = {
				'group': group,
				'users': users,
			}

			return render(request, 'group_summary.html', context_dict)
		else:
			return render(request, 'groups.html')
	# Change the following line to a general groups page later on.
	return HttpResponse('Inappropriate arrival at /group')
