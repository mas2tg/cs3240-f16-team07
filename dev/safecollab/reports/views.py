from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from reports.models import Report, ReportForm
from django.db.models import Q
from django.utils.encoding import smart_str
from django.http import StreamingHttpResponse
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def index(request):
    username = request.user
    category_list = Report.objects.filter(creator=username)
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

def add_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return HttpResponseRedirect('/see-reports')
        else:
            # The supplied form contained errors - just print them to the terminal.
            print (form.errors)
    else:
        # This should never happen
        return HttpResponse('Improper arrival at add_report, see reports.views')


def download(request,link_to_file):
      path = os.path.join(BASE_DIR, 'media')
      path += "/attachments"
      filename=link_to_file

#       response = HttpResponse(content_type='application/force-download')
#       response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(link_to_file)
#       response['X-Sendfile'] = smart_str(path)
# # It's usually a good idea to set the 'Content-Length' header too.
# # You can also set any other required headers: Cache-Control, etc.
#       return response

      file_full_path = path+"/{0}".format(filename)

      response = StreamingHttpResponse((line for line in open(file_full_path,'r')))
      response['Content-Disposition'] = "attachment; filename={0}".format(filename)
      response['Content-Length'] = os.path.getsize(file_full_path)
      return response




      # def file_iterator(file_name, chunk_size=512):
      #   with open(file_name) as f:
      #     while True:
      #       c = f.read(chunk_size)
      #       if c:
      #         yield c
      #       else:
      #         break
      # response = StreamingHttpResponse(file_iterator(filename))
      # response['Content-Type'] = 'application/octet-stream'
      # response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
      # return response
