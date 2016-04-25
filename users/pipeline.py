from django.shortcuts import redirect
from social.pipeline.partial import partial


@partial
def get_additional_user_info(strategy, details, user=None, *args, **kwargs):
	if user:
		return {'is_new': False}

	backend = kwargs.get('backend')
	response = kwargs.get('response')

	print(str(response).encode('utf-8'))

	print(backend.name)

	partial_user_data = {}

	if backend.name == 'facebook':
		if 'first_name' in response and 'last_name' in response:
			partial_user_data['first_name'] = response['first_name']
			partial_user_data['last_name'] = response['last_name']
		elif 'name' in response:
			name = response['name']
			i = name.rindex(' ')
			if i >= 0:
				partial_user_data['first_name'] = name[:i]
				partial_user_data['last_name'] = name[i+1:]
			else:
				partial_user_data['first_name'] = name
		if 'email' in response:
			partial_user_data['email'] = response['email']

	if backend.name == 'twitter':
		if 'name' in response:
			name = response['name']
			i = name.rindex(' ')
			if i >= 0:
				partial_user_data['first_name'] = name[:i]
				partial_user_data['last_name'] = name[i+1:]
			else:
				partial_user_data['first_name'] = name
		if 'email' in response:
			partial_user_data['email'] = response['email']

	if backend.name == 'google-oauth2':
		if 'name' in response:
			name = response['name']
			if 'givenName' in name:
				partial_user_data['first_name'] = name['givenName'].capitalize()
			if 'familyName' in name:
				partial_user_data['last_name'] = name['familyName'].capitalize()
			elif 'displayName' in response:
				name = response['displayName']
				i = name.rindex(' ')
				if i >= 0:
					partial_user_data['first_name'] = name[:i].capitalize()
					partial_user_data['last_name'] = name[i+1:].capitalize()
				else:
					partial_user_data['first_name'] = name.capitalize()
		if 'emails' in response:
			emails = response['emails']
			if len(emails) > 0:
				email = response['emails'][0]
				if 'value' in email:
					partial_user_data['email'] = email['value']


	if backend.name == 'facebook' or backend.name == 'twitter' or backend.name == 'google-oauth2':
		strategy.session_set('partial_user_data', partial_user_data)

	return redirect('/users/register-social')

def create_user(strategy, details, user=None, *args, **kwargs):
	if user:
		return {'is_new': False}

	return {
		'is_new': True,
		'user': kwargs.get('request').user,
	}

