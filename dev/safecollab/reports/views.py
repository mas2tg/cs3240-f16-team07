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


