from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from reports.models import Report, ReportForm
from django.db.models import Q
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def index(request):
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

    context_dict = {'reports':category_list,"type":queryType}
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    return render(request, 'reports.html', context_dict)


def detail(request,file_name):
    report = Report.objects.filter(name=file_name)
    test = True if edit else False
    context_dict = {'reports':report}

    return render(request, 'detail.html', context_dict)

def edit(request,file_name): #TODO: figure out how to include POST in request
    report=get_object_or_404(Report, name=file_name)
    # form = ReportForm(request.POST, intance=report)
    if request.method== "POST":
        #report = report.save(commit=False)
        report.name = request.POST.get('name')
        report.description = request.POST.get('description')
        report.longDescription = request.POST.get('longDescription')
        report.path = request.POST.get('path')
        report.private = request.POST.get('private')
        report.encrypted = request.POST.get('encrypted')
        report.save()
        return HttpResponseRedirect('/reports')
    else:
        context_dict = {'reports':report}
        return render(request, 'edit.html', context_dict)

            #return render(request, 'detail.html', context_dict)



def add_report(request):
        if request.method == 'POST':
                form = ReportForm(request.POST, request.FILES)
                creator = request.user
                name = request.POST.get('name')
                description = request.POST.get('description')
                path = request.FILES.get('path')
                encrypted = True if request.POST.get('encrypted') else False
                longDescription = request.POST.get('longDescription')
                private = True if request.POST.get('private') else False

                report = Report(creator_id=creator.id, encrypted=encrypted, name=name, description=description, path=path,longDescription=longDescription,private =private)

                # Now we save the UserProfile model instance.
                report.save()

                return HttpResponseRedirect('/reports')

        else:
                # This should never happen
                return HttpResponse('Improper arrival at add_report, see reports.views')






def download(request,link_to_file):
      path = os.path.join(BASE_DIR, 'media')
      path += "/attachments"
      filename=link_to_file

      response = HttpResponse(content_type='application/force-download')
      response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(link_to_file)
      response['X-Sendfile'] = smart_str(path)
# It's usually a good idea to set the 'Content-Length' header too.
# You can also set any other required headers: Cache-Control, etc.
      return response


