from django.contrib.auth import logout

class ForceLogoutMiddleware(object):
	def process_request(self, request):
		if request.user.is_authenticated() and not request.user.is_active:
			logout(request)