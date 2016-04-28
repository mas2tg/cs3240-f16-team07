from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from reports.models import Report, ReportForm, Folder, FileForm, File
#from auth.models
from django.db.models import Q
from django.utils.encoding import smart_str
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def index(request, folder_name='$'):
    username = request.user
    if(folder_name=='$'):
        if(request.user.has_perm('users.site_manager')):
            category_list = Report.objects.all()
        else:
            category_list = Report.objects.filter((Q(private=False) & ~Q(creator=username)) | (Q(creator=username) & Q(folder=None)) )



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
    
        


def detail(request,file_name):
    report = Report.objects.filter(name=file_name)

    has_permission= (request.user.has_perm('users.site_manager'))
    files = (File.objects.filter(report=report))
    context_dict = {'reports':report,"has_permission":has_permission,"files":files}


    return render(request, 'detail.html', context_dict)

def edit(request,file_name): #TODO: implement delete option for individual files
    report=get_object_or_404(Report, name=file_name)
    file=File.objects.filter(report=report)
    obj_list = Folder.objects.filter(creator=request.user)
    is_owner = report.creator == request.user
    # form = ReportForm(request.POST, intance=report)
    
    if request.method== "POST":
        #report = report.save(commit=False)
        report.name = request.POST.get('name')
        report.description = request.POST.get('description')
        report.longDescription = request.POST.get('longDescription')
        report.private = True if request.POST.get('private') else False
        report.encrypted = True if request.POST.get('encrypted') else False
        folder_obj = get_object_or_404(Folder, name=request.POST.get('folder'))
        report.folder= folder_obj


        report.save()
        
        paths = request.FILES.getlist('path')
        #print(request)
        for path in paths:
            File(report=report, path=path).save() #pass variables to fields

        

        return HttpResponseRedirect('/reports/$/')
    else:
        context_dict = {'reports':report,'folders':obj_list,'is_owner':is_owner,'files':file}

        return render(request, 'edit.html', context_dict)

            #return render(request, 'detail.html', context_dict)

def delete(request,file_name): #Delete reports #TODO: implement delete files separately
    
    report=get_object_or_404(Report, name=file_name)
    file=File.objects.filter(report=report).delete() # delete files from report first!
    report.delete()
    
    return HttpResponseRedirect('/reports/$/')

def delete_file(request, path, report_name):
    File.objects.filter(path=path).delete() #must query by report and by name

    #print(files)
    report=get_object_or_404(Report, name=report_name)
    obj_list = Folder.objects.filter(creator=request.user)
    file=File.objects.filter(report=report)
    is_owner = report.creator == request.user

    context_dict = {'reports':report,'folders':obj_list,'is_owner':is_owner,'files':file}
    return render(request, 'edit.html', context_dict)
    #return HttpResponse("File deleted!")

def add_report(request): #the user is able to select multiple files
        if request.method == 'POST':
                form = ReportForm(request.POST, request.FILES)
                creator = request.user
                name = request.POST.get('name')
                description = request.POST.get('description')
                
                encrypted = True if request.POST.get('encrypted') else False
                longDescription = request.POST.get('longDescription')
                private = True if request.POST.get('private') else False

                report = Report(creator_id=creator.id, encrypted=encrypted, name=name, description=description,longDescription=longDescription,private =private)

                
                
                # Now we save the UserProfile model instance.
                report.save()

                #file = File(report=report, path=paths) #pass variables to fields
                
                paths = request.FILES.getlist('path')
                #print(request.FILES)
                for path in paths:
                    File(report=report, path=path).save() #pass variables to fields
                    
                #file.save()

                return HttpResponseRedirect('/reports/$/')

        else:
                # This should never happen
                return HttpResponse('Improper arrival at add_report, see reports.views')


def add_folder(request):
    #TODO: implement if statement for POST
    folderName = request.POST.get("folderName")
    creator = request.user
    folder = Folder(creator=creator,name=folderName)
    folder.save()
    return HttpResponseRedirect('/reports/$/')


def download(request,link_to_file): #TODO:download is still not working
#       path = os.path.join(BASE_DIR, 'media')
#       path += "/attachments"
#       filename=link_to_file
#
#       response = HttpResponse(content_type='application/force-download')
#       response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(link_to_file)
#       response['X-Sendfile'] = smart_str(path)
# # It's usually a good idea to set the 'Content-Length' header too.
# # You can also set any other required headers: Cache-Control, etc.
#       return response
    response = HttpResponse(content_type='application/force-download') # mimetype is replaced by content_type for django 1.7
    response['Content-Disposition'] = 'attachments; filename=%s' % smart_str(link_to_file)
    response['X-Sendfile'] = smart_str(link_to_file)
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response

