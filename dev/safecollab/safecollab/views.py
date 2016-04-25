from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group, Permission
from users.models import UserForm, UserProfileForm
from reports.models import Report, ReportForm
from social.backends.utils import load_backends
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
"""
def index(request,folder_name):
    if(folder_name=='$'):
        username = request.user
        category_list = Report.objects.filter(Q(private=False) | Q(creator=username))

        # Query the database for a list of ALL categories currently stored.
        # Order the categories by no. likes in descending order.
        # Retrieve the top 5 only - or all if less than 5.
        # Place the list in our context_dict dictionary which will be passed to the template engine.

        queryType = request.GET.get("type")
        query = request.GET.get("q")
        if(query):
            if (queryType=="name"):

                category_list = category_list.filter(Q(name__icontains=query))
            elif (queryType=="description"):
                category_list = category_list.filter(Q(description__icontains=query))
        folder_list = Folder.objects.all();
        context_dict = {'reports':category_list,"type":queryType,'folders':folder_list}
        # Return a rendered response to send to the client.
        # We make use of the shortcut function to make our lives easier.
        # Note that the first parameter is the template we wish to use.

        return render(request, 'reports.html', context_dict)
    else:
        folder = Folder.objects.get(name=folder_name)
        category_list = Report.objects.filter(folder=folder.id)
        context_dict = {'reports':category_list}
        return render(request, 'reports.html', context_dict)
"""

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
