from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from inbox.models import Message
from crypto.models import AESCipher
import os

def index(request):
	return render(request, 'inbox.html', {})

def send(request):
	if request.method == 'POST':
		sender = request.user
		recipient = User.objects.get(username=request.POST.get('recipient'))
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
		return HttpResponse('Improper arrival at send, see inbox.views')

def delete(request):
	if request.method == 'POST':
		message_ids = request.POST.getlist('message_ids[]')
		for message_id in message_ids:
			print(message_id)
			Message.objects.get(id=message_id)
			print('test')
			Message.objects.get(id=message_id).delete()
		
		print('test')
		unread = request.user.get_unread_messages()
		data = {
			'message_count': unread.count(),
		}
		return JsonResponse(data)

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
		return JsonResponse(data)

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
		return JsonResponse(data)

	else:
		# This should never happen
		return HttpResponse('Improper arrival at mark_as_unread, see inbox.views')

def decrypt(request):
	if request.method == 'POST':
		message_id = request.POST.get('message_id')
		message = Message.objects.get(id=message_id)
		raw = AESCipher(bytes(message.key)).decrypt(message.body).decode('utf-8')
		data = {
			'raw': raw,
		}
		return JsonResponse(data)

	else:
		# This should never happen
		return HttpResponse('Improper arrival at mark_as_unread, see inbox.views')
