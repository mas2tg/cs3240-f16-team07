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
	if request.user and request.user.is_authenticated():
		return HttpResponseRedirect('/home/')
	context_dict = {
		'user_form': UserForm(),
		'profile_form': UserProfileForm(),
	}
	return render(request, 'index.html', context_dict)

def about(request):
	return render(request, 'about.html')

def contact(request):
	return render(request, 'contact.html')

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
	return render(request, 'home.html', {})

def strToOperator(s):
	if s == 'AND':
		return '&'
	if s == 'OR':
		return '|'
	return '&'
def refine(query, current_string, current_mode, not_mode, params):
	if len(current_string) > 0:
		query_part = None
		namespace = {'Q': Q, 'query_part':query_part}
		exec('query_part = Q(' + params[0] + '__icontains="' + current_string + '")', namespace)
		query_part = namespace['query_part']
		for param in params[1:]:
			namespace = {'Q': Q, 'query_part':query_part}
			exec('query_part |= Q(' + param + '__icontains="' + current_string + '")', namespace)
			query_part = namespace['query_part']
		namespace = {'query': query, 'query_part':query_part}
		exec('query ' + strToOperator(current_mode) + '= ' + ('~' if not_mode else '') + 'query_part', namespace)
		query = namespace['query']
	return query
def make_query(raw, params):
	current_string = ''
	current_mode = 'AND'
	not_mode = False
	query = Q()
	for token in raw.split():
		if token == 'AND':
			query = refine(query, current_string, current_mode, not_mode, params)
			current_string = ''
			not_mode = False
			current_mode = 'AND'
			continue
		if token == 'OR':
			query = refine(query, current_string, current_mode, not_mode, params)
			current_string = ''
			not_mode = False
			current_mode = 'OR'
			continue
		if token == 'NOT':
			not_mode = True
			continue
		if current_string == '': current_string = token
		else: current_string += ' ' + token
	return refine(query, current_string, current_mode, not_mode, params)
@login_required
def search(request):
	if request.method == "POST":
		query_type = request.POST.get('query_type','All')
		raw_query = request.POST.get('query','')
		
		context_dict = { 'query_type': query_type }

		user_params = ['username', 'first_name', 'last_name', 'email']
		report_params = ['name', 'description', 'longDescription']
		group_params = ['name']

		if query_type == 'All':
			context_dict['user_results'] = User.objects.filter( make_query(raw_query, user_params) )
			context_dict['report_results'] = Report.objects.filter( make_query(raw_query, report_params) )
			context_dict['group_results'] = Group.objects.filter( make_query(raw_query, group_params) )
			if not request.user.has_perm('users.site_manager'):
				context_dict['group_results'] &= request.user.groups.all()

		elif query_type == 'Users':
			context_dict['user_results'] = User.objects.filter( make_query(raw_query, user_params) )
		elif query_type == 'Reports':
			context_dict['report_results'] = Report.objects.filter( make_query(raw_query, report_params) )
		elif query_type == 'Groups':
			context_dict['group_results'] = Group.objects.filter( make_query(raw_query, group_params) )
			if not request.user.has_perm('users.site_manager'):
				context_dict['group_results'] &= request.user.groups.all()
		else:
			context_dict['user_results'] = User.objects.filter( make_query(raw_query, user_params) )
			context_dict['report_results'] = Report.objects.filter( make_query(raw_query, report_params) )
			context_dict['group_results'] = Group.objects.filter( make_query(raw_query, group_params) )
			if not request.user.has_perm('users.site_manager'):
				context_dict['group_results'] &= request.user.groups.all()

		return render(request, 'search.html', context_dict)
	
	return render(request, 'search.html', {})

@login_required
def groups(request, **kwargs):
	group_ids = set([ group.id for group in request.user.groups.all() ])
	context_dict = {
		'favorite_groups': UserProfile.objects.get(user__id=request.user.id).favorite_groups.all(),
		'other_groups': Group.objects.filter(~Q(id__in=group_ids)),
	}

	if 'error_messages' in kwargs:
		context_dict['error_messages'] = kwargs['error_messages']

	return render(request, 'groups.html', context_dict)

@login_required
def group_summary(request, group_id, **kwargs):
	query_set = Group.objects.filter(id=int(group_id))
	if query_set.exists():
		group = query_set[0]
		users = group.user_set.all()

		if not request.user.has_perm('users.site_manager') and request.user not in users:
			error_messages = ['You do not have permission to view group ' + str(group.name) + '.']
			return safecollab.views.group(request, error_messages=error_messages)

		context_dict = {
			'group': group,
			'users': users,
			'is_member': request.user.groups.filter(id=int(group_id)).exists(),
		}
		
		if 'error_messages' in kwargs:
			context_dict['error_messages'] = kwargs['error_messages']

		return render(request, 'group_summary.html', context_dict)
	else:
		return HttpResponseRedirect('/groups')