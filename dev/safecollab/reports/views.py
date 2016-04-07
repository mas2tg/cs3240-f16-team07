from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from reports.models import ReportForm

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


