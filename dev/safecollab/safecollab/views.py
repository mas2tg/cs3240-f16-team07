from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from users.models import RegisterForm

def index(request):
    context_dict = {
    	'boldmessage': "I am bold font from the context",
    }
    return render(request, 'index.html', context_dict)

def register(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data or send to database
        	form.save(commit=True)
        	# redirect to new URL:
        	return HttpResponseRedirect('/index/')
        else:
        	print(form.errors)
    else:
        form = RegisterForm()

    context_dict = {
    	'form': form,
    }

    return render(request, 'register.html', context_dict)
