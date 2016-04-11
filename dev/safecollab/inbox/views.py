from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from inbox.models import Message
import json

def index(request):
	return render(request, 'inbox.html', {})

def send(request):
	if request.method == 'POST':
		sender = request.user
		recipient = User.objects.get(username=request.POST.get('recipient'))
		body = request.POST.get('body')

		message = Message(sender=sender, recipient=recipient, body=body)
		message.save()

		return HttpResponseRedirect('/inbox')

	else:
		# This should never happen
		return HttpResponse('Improper arrival at send, see inbox.views')

def delete(request):
	if request.method == 'POST':
		message_ids = request.POST.getlist('message_ids[]')
		for message_id in message_ids:
			Message.objects.get(id=message_id).delete()
		
		unread = request.user.get_unread_messages()
		data = {
			'message_count': unread.count(),
		}
		return HttpResponse(json.dumps(data))

	else:
		# This should never happen
		return HttpResponse('Improper arrival at delete, see inbox.views')

def mark_as_read(request):
	if request.method == 'POST':
		message_ids = request.POST.getlist('message_ids[]')
		for message_id in message_ids:
			message = Message.objects.get(id=message_id)
			message.read = True
			message.save()
		unread = request.user.get_unread_messages()
		data = {
			'message_count': unread.count(),
		}
		return HttpResponse(json.dumps(data))

	else:
		# This should never happen
		return HttpResponse('Improper arrival at mark_as_read, see inbox.views')

def mark_as_unread(request):
	if request.method == 'POST':
		message_ids = request.POST.getlist('message_ids[]')
		for message_id in message_ids:
			message = Message.objects.get(id=message_id)
			message.read = False
			message.save()

		unread = request.user.get_unread_messages()
		data = {
			'message_count': unread.count(),
		}
		return HttpResponse(json.dumps(data))

	else:
		# This should never happen
		return HttpResponse('Improper arrival at mark_as_unread, see inbox.views')