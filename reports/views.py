from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from reports.models import Report, ReportForm, Folder, FileForm, File
#from auth.models
from django.db.models import Q
from django.utils.encoding import smart_str
# from django_geoip.models import IpRange
import pygeoip
import os
from safecollab import settings
from django.http import HttpRequest
from django.contrib.auth.models import User, Group

def index(request, folder_name='$'):
    username = request.user
    group = username.groups.all()
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
                search = query.split()
                if "and" in search:
                    x=search.index('and')
                    category_list=category_list.filter(Q(name__icontains=search[x-1]))
                    category_list=category_list.filter(Q(name__icontains=search[x+1]))
                elif "or" in search:
                    x=search.index('or')
                    category_list=category_list.filter(Q(name__icontains=search[x-1])| Q(name__icontains=search[x+1]))
                elif "not" in search:
                    x=search.index('not')
                    category_list=category_list.filter(~Q(name__icontains=search[x+1]))

                else:
                    category_list = category_list.filter(Q(name__icontains=query))
            elif (queryType=="description"):

                search = query.split(" ")
                if "and" in search:
                    x=search.index('and')
                    category_list=category_list.filter(Q(description__icontains=search[x-1]))
                    category_list=category_list.filter(Q(description__icontains=search[x+1]))
                elif "or" in search:
                    x=search.index('or')
                    category_list=category_list.filter(Q(description__icontains=search[x-1])| Q(description__icontains=search[x+1]))
                elif "not" in search:
                    x=search.index('not')
                    category_list=category_list.filter(~Q(description__icontains=search[x+1]))

                else:
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


    reports_user_can_access = Report.objects.filter(Q(creator=request.user) | Q(private=False))
    if not request.user.has_perm('users.site_manager'):
        for user in User.objects.filter(groups__in=request.user.groups.all()):
            reports_user_can_access |= Report.objects.filter(creator=user)
    
    has_permission = report[0] in reports_user_can_access

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
        report.keyword = request.POST.get('keyword')
        report.description = request.POST.get('description')
        report.longDescription = request.POST.get('longDescription')
        report.private = True if request.POST.get('private') else False
        report.encrypted = True if request.POST.get('encrypted') else False

        folder_obj = None
        query_set = Folder.filter(name=request.POST.get('folder'))
        if not query_set.exists():
            folder_obj = query_set[0]
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

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def add_report(request): #the user is able to select multiple files
        if request.method == 'POST':
                form = ReportForm(request.POST, request.FILES)
                creator = request.user
                name = request.POST.get('name')
                keyword = request.POST.get('keyword')
                description = request.POST.get('description')
                
                encrypted = True if request.POST.get('encrypted') else False
                longDescription = request.POST.get('longDescription')
                private = True if request.POST.get('private') else False

                ip = get_client_ip(request)



                file = os.path.join(settings.GEOIP_PATH, 'GeoLiteCity.dat')

                
                gi = pygeoip.GeoIP(file)
                info=gi.record_by_addr(ip)
                
                
                
                area_code = None
                city = None
                country = None
                if info != None:
                    area_code = info['region_code']
                    city = info['city']
                    country = info['country_name']


                report = Report(creator_id=creator.id,region_code=area_code,city=city,country=country,keyword=keyword, encrypted=encrypted, name=name, description=description,longDescription=longDescription,private =private)

                #
                report.save()
                # file = File(report=report, path=paths) #pass variables to fields

                paths = request.FILES.getlist('path')
                #print(request.FILES)
                for path in paths:
                    File(report=report, path=path).save() #pass variables to fields


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

def delete_folder(request,folder_id):

    folder=get_object_or_404(Folder,id=folder_id)
    reports_list = Report.objects.filter(folder=folder)
    for report in reports_list:
        report.folder= None
    folder.delete()
    return HttpResponseRedirect('/reports/$/')