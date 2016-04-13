from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from reports.models import Report, ReportForm

def index(request):
	# Query the database for a list of ALL categories currently stored.
	# Order the categories by no. likes in descending order.
	# Retrieve the top 5 only - or all if less than 5.
	# Place the list in our context_dict dictionary which will be passed to the template engine.

	category_list = Report.objects.all()
	context_dict = {'reports':category_list, }
	# Return a rendered response to send to the client.
	# We make use of the shortcut function to make our lives easier.
	# Note that the first parameter is the template we wish to use.

	return render(request, 'reports.html', context_dict)

def add_report(request):
    if request.method == 'POST':
		form = ReportForm(request.POST, request.FILES)

		creator = request.user
		name = request.POST.get('name')
		description = request.POST.get('description')
		path = request.FILES.get('path')
		encrypted = True if request.POST.get('encrypted') else False

		report = Report(creator_id=creator.id, encrypted=encrypted, name=name, description=description, path=path)

		# Now we save the UserProfile model instance.
		report.save()

		return HttpResponseRedirect('/reports')

	else:
		# This should never happen
		return HttpResponse('Improper arrival at add_report, see reports.views')





def download(request,link_to_file):
      path = os.path.join(BASE_DIR, 'media')
      path =os.path.join(path,'attachments')
      filename=link_to_file

      response = HttpResponse(content_type='application/force-download')
      response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(link_to_file)
      response['X-Sendfile'] = smart_str(path)
# It's usually a good idea to set the 'Content-Length' header too.
# You can also set any other required headers: Cache-Control, etc.
      return response
