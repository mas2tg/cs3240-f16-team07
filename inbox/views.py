from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from inbox.models import Message
from crypto.models import AESCipher
import os

@login_required
def index(request, **kwargs):
	context_dict = {}
	if 'error_messages' in kwargs:
		context_dict['error_messages'] = kwargs['error_messages']
	return render(request, 'inbox.html', context_dict)

@login_required
def send(request):
	if request.method == 'POST':
		sender = request.user
		query_set = User.objects.filter(username=request.POST.get('recipient'))
		if not query_set.exists():
			return index(request, error_messages = ['User "' + str(request.POST.get('recipient')) + '" could not be found.']) 
		recipient = query_set[0]
		body = request.POST.get('body')
		encrypt = True if request.POST.get('encrypt') else False
		key = None

		if encrypt:
			key = os.urandom(32)
			body = AESCipher(key).encrypt(body).decode('utf-8')

		message = Message(sender=sender, recipient=recipient, body=body, encrypted=encrypt, key=key)
		message.save()

		return HttpResponseRedirect('/inbox')

	else:
		# This should never happen
		return index(request, error_messages = ['Invalid request.'])

@login_required
def delete(request):
	if request.method == 'POST':
		message_ids = request.POST.getlist('message_ids[]')
		for message_id in message_ids:
			message = Message.objects.get(id=message_id)
			if message.recipient != request.user:
				return index(request, error_messages = ['You are not authorized to modify ' + ('this message.' if len(message_ids) == 1 else 'these messages.')])
			message.delete()
		
		unread = request.user.get_unread_messages()
		data = {
			'message_count': unread.count(),
		}
		return JsonResponse(data)

	else:
		# This should never happen
		return index(request, error_messages = ['Invalid request.'])

@login_required
def mark_as_read(request):
	if request.method == 'POST':
		message_ids = request.POST.getlist('message_ids[]')
		for message_id in message_ids:
			message = Message.objects.get(id=message_id)
			if message.recipient != request.user:
				return index(request, error_messages = ['You are not authorized to modify ' + ('this message.' if len(message_ids) == 1 else 'these messages.')])
			message.read = True
			message.save()
		unread = request.user.get_unread_messages()
		data = {
			'message_count': unread.count(),
		}
		return JsonResponse(data)

	else:
		# This should never happen
		return index(request, error_messages = ['Invalid request.'])

@login_required
def mark_as_unread(request):
	if request.method == 'POST':
		message_ids = request.POST.getlist('message_ids[]')
		for message_id in message_ids:
			message = Message.objects.get(id=message_id)
			if message.recipient != request.user:
				return index(request, error_messages = ['You are not authorized to modify ' + ('this message.' if len(message_ids) == 1 else 'these messages.')])
			message.read = False
			message.save()

		unread = request.user.get_unread_messages()
		data = {
			'message_count': unread.count(),
		}
		return JsonResponse(data)

	else:
		# This should never happen
		return index(request, error_messages = ['Invalid request.'])

@login_required
def decrypt(request):
	if request.method == 'POST':
		message_id = request.POST.get('message_id')
		message = Message.objects.get(id=message_id)
		if message.recipient != request.user:
			return index(request, error_messages = ['You are not authorized to modify this message.'])
		raw = AESCipher(bytes(message.key)).decrypt(message.body).decode('utf-8')
		data = {
			'raw': raw,
		}
		return JsonResponse(data)

	else:
		# This should never happen
		return index(request, error_messages = ['Invalid request.'])
