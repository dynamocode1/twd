from django import forms
from django.contrib.auth.forms import BaseUserCreationForm
from .models import User,Course,Blog
from mezzanine.core.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from  django_summernote.widgets import SummernoteWidget
class TopicForm(forms.Form):
    title = forms.CharField(max_length=200,widget = forms.TextInput({'class':'form-control'}))
    content = forms.CharField(widget=CKEditorWidget(attrs = {'class':'form-control'}))
class NewCourseForm(forms.Form):
	image = forms.FileField(widget = forms.FileInput(attrs = {'class':'form-control'}),required= False)
	title = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control'}))
	description = forms.CharField(widget = forms.Textarea(attrs = {'class':'form-control'}))
	
class SignUpForm(BaseUserCreationForm):
	password1 = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control'}))
	password2 = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control'}))

	class Meta:
		model = User
		fields = ['lname','fname','email','password1','password2','username']
		widgets = {'lname':forms.TextInput(attrs = {'class':'form-control'}),
				    'fname':forms.TextInput(attrs = {'class':'form-control'}),
				    'email':forms.EmailInput(attrs = {'class':'form-control'}),
				    'username':forms.TextInput(attrs = {'class':'form-control'})



		}

	def clean_email(self):
		email = self.cleaned_data['email']
		indx = email.find('@')
		data = email[indx+1:]
		if data != 'gmail.com':
			raise forms.ValidationError('Use a gmail account')
		return email
	def save(self,commit = True):
		lname = self.cleaned_data['lname']
		fname = self.cleaned_data['fname']
		uname = self.cleaned_data['username']

		user = super().save(commit = False)
		user.username = uname
		user.fname = fname
		user.lname = lname

		if commit:
			user.save()
			return user
class NewBlogForm(forms.Form):
	title = forms.CharField(max_length=200,widget = forms.TextInput({'class':'form-control'}))
	image = forms.FileField(widget = forms.FileInput(attrs = {'class':'form-control'}),required= False)
	body = forms.CharField(widget=CKEditorWidget(attrs = {'class':'form-control'}))
class AdminLoginForm(forms.Form):
	username = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control'}))
	password = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control'}))

class LoginForm(forms.Form):
	email = forms.CharField(widget = forms.EmailInput(attrs = {'class':'form-control'}))
	password = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control'}))