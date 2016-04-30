from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group, Permission
from users.models import UserProfile, UserForm, UserProfileForm
from reports.models import Report, ReportForm, Folder
from django.db.models import Q
from django.conf import settings
from django.core import serializers

def index(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/home')

	context_dict = {
		'user_form': UserForm(),
		'profile_form': UserProfileForm(),
	}
	return render(request, 'index.html', context_dict)

def fda_index(request):
        username = request.GET.get('username',default="Do not exist")
        username = User.objects.filter(username=username)
        category_list = Report.objects.filter(Q(private=False) | Q(creator=username))
        #context_dict = {'reports':category_list,"type":queryType)
        #return HttpResponse("Hello from fda_index %s" % username)
        #print(category_list)
        json_data = serializers.serialize("json",category_list)
        return HttpResponse(json_data,content_type='application/json')

@login_required
def home(request):
	obj_list = Folder.objects.filter(creator=request.user)
	context_dict = {
		'form': ReportForm(),
		'folders': obj_list,
	}
	return render(request, 'home.html', context_dict)

def process_query(raw):
	current_string = ''
	query = Q()
	for token in raw.split():
		if token.toUpper() == 'AND':
			query = query & Q
def search(request):
	if request.method == "POST":
		query_type = request.POST.get('query_type','All')
		query = request.POST.get('query','')
		
		context_dict = { 'query_type': query_type }
		
		if query_type == 'All':
			context_dict['user_results'] = User.objects.filter()
			context_dict['report_results'] = Report.objects.filter()
			context_dict['group_results'] = Group.objects.filter()
		elif query_type == 'Users':
			context_dict['user_results'] = User.objects.filter()
		elif query_type == 'Reports':
			context_dict['report_results'] = Report.objects.filter()
		elif query_type == 'Groups':
			context_dict['group_results'] = Group.objects.filter()
		else:
			context_dict['user_results'] = User.objects.filter()
			context_dict['report_results'] = Report.objects.filter()
			context_dict['group_results'] = Group.objects.filter()

		return render
	else:
		return HttpResponseRedirect('')

def groups(request):
	group_ids = set([ group.id for group in request.user.groups.all() ])
	context_dict = {
		'favorite_groups': UserProfile.objects.get(user__id=request.user.id).favorite_groups.all(),
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