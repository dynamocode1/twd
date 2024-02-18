from django.conf import settings
from django import http
class CoreMiddleWare:
	def __init__(self,get_response):
		self.get_response = get_response

	def __call__(self,request):
		resp = self.get_response(request)
		print(request.COOKIES)
		if settings.DEVELOPMENT_MODE:
			return http.HttpResponse('This Site is Under Development')
		return resp