from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group, Permission
from users.models import UserProfile, UserForm, UserProfileForm
from reports.models import Report, ReportForm, Folder
from django.db.models import Q

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
	obj_list = Folder.objects.filter(creator=request.user)
	return render(request, 'home.html', {
		'form': ReportForm(),
		'folders': obj_list,
		})

def groups(request):
	group_ids = set([ group.id for group in request.user.groups.all() ])
	context_dict = {
		'other_groups': Group.objects.filter(~Q(id__in=group_ids)),
	}
	return render(request, 'groups.html', context_dict)

def group_summary(request, group_id):
	query_set = Group.objects.filter(id=int(group_id))
	if query_set.exists():
		group = query_set[0]
		users = group.user_set.all()

		context_dict = {
			'group': group,
			'users': users,
			'is_member': request.user.groups.filter(id=int(group_id)).exists(),
		}
		
		return render(request, 'group_summary.html', context_dict)
	else:
		return HttpResponseRedirect('/groups')
