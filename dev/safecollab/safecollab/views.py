from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group, Permission
from users.models import UserForm, UserForm, UserProfileForm
from reports.models import Report, ReportForm

def index(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/home')

	context_dict = {
		'boldmessage': "I am bold font from the context",
		'user_form': UserForm(),
		'profile_form': UserProfileForm(),
	}
	return render(request, 'index.html', context_dict)

@login_required
def home(request):
	return render(request, 'home.html', {
		'form': ReportForm(),
		})

def groups(request):
	if request.method == 'GET':
		group_name = request.GET.get('name')
		group = Group.objects.get(name=group_name)
		users = group.user_set.all()

		context_dict = {
			'group': group,
			'users': users,
		}

		return render(request, 'group_summary.html', context_dict)
	# Change the following line to a general groups page later on.
	return HttpResponse('Inappropriate arrival at /group')


def reports(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.

    category_list = Report.objects.all()
    context_dict = {'reports': category_list}
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    return render(request, 'reports.html', context_dict)