from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

def index(request):
	return render(request, 'inbox.html', {})

def send(request):
	if request.method == 'POST':
		pass

	else:
		# This should never happen
		return HttpResponse('Improper arrival at send, see inbox.views')
