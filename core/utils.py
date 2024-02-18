from .models import User
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.core.exceptions import ValidationError
def admin_required(func):
	def wrapper(request,*args,**kwargs):
		admin =  request.session.get('admin')
		if admin == None:
			return redirect('no_perm')
		if admin:
			if request.COOKIES['admin_id'] != admin:
				return redirect('no_perm')
		
		return func(request,*args,**kwargs)
	return wrapper
def authenticate_admin(request):
	session_id = get_random_string(32)
	
	request.session['admin'] = session_id
	return session_id
	

class UserMixin(LoginRequiredMixin,UserPassesTestMixin):
	login_url = reverse_lazy('register')
	def test_func(self):
		black_list = []
		return self.request.user not in black_list
class Auth(ModelBackend):
	def authenticate(self,request,email,password,**kwargs):
		userObj = self.get_user_model()

		try:
			user = userObj.objects.get(email = email)
		except userObj.DoesNotExists:
			raise ValidationError('User Does Not Exists')
		if user.check_password(password):
			return user
		else: 
			raise ValidationError('Incorrect Password')
			
	def get_user(self,user_id):
		userObj = self.get_user_model()
		try: 
			return userObj.objects.get(id = user_id)
		except:
			return None

