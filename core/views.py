from django.shortcuts import render,redirect
from django.views import generic
from .forms import SignUpForm
from django.contrib.auth import login,authenticate
from django.db import transaction
from .models import Blog,Course
from django.db.models import Q
from .utils import UserMixin
from .forms import LoginForm
class Home(generic.TemplateView):
	template_name = 'pages/home.html'

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		blogs = Blog.objects.all()[:12]
		context['blogs'] = blogs
		return context
class About(generic.TemplateView):
	template_name = 'pages/about.html'

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		blogs = Blog.objects.all()[:12]
		context['blogs'] = blogs
		return context
class Courses(UserMixin,generic.TemplateView):
	template_name = 'pages/courses.html'

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		obj = Course.objects.filter(pub = True).all()
		context['objects'] = obj

		return context
class Blogs(generic.ListView):
	template_name = 'pages/blogs.html'
	model = Blog
	context_object_name = 'blogs'
	def get_queryset(self):
		
		query = self.request.GET.get('q')
		if query:
			qs = Q(title__contains = query)|Q(title__icontains = query)
			query = Blog.objects.filter(qs).all()
			return query
		else:
			qs = Blog.objects.all()
			return qs



class ReadBlog(generic.DetailView):
	template_name = 'pages/read_blogs.html'
	model = Blog
	context_object_name = 'blog'

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		recommended_blogs = Blog.objects.order_by('?')
		context['r_blogs'] = recommended_blogs
		return context

class CoursesSearch(UserMixin,generic.View):
	template_name = 'pages/courses.html'
	context = {}
	def get(self,request,*args,**kwargs):
		parameter = request.GET.get('query')
		query = Course.objects.filter(pub = True).all()
		self.context['objects'] = query
		self.context['q'] = parameter
		if parameter:
			queryset = Q(title__contains = parameter) | Q(description__contains = parameter)
			query = Course.objects.filter(queryset).filter(pub = True)
			print(query)
			self.context['objects'] = query
			self.context['q'] = parameter
			return render(request,self.template_name,self.context)
		return render(request,self.template_name,self.context)

class LearnCourse(UserMixin,generic.View):
	template_name = 'pages/course.html'
	context = {}

	def get(self,request,id,*args,**kwargs):
		obj = Course.objects.get(id = id)
		if not obj.is_pub:
			return redirect('courses')
		topics = obj.topics
		self.context['course'] = obj
		self.context['topics'] = topics
		self.context['id'] = id
		topic = request.GET.get('topic')
		if topic:
			self.context['topic'] = topics.get(id = int(topic))
		else:
			self.context['topic'] = topics.first()
		print(self.context['topic'])
		return render(request,self.template_name,self.context)
class Register(generic.View):
	template_name = 'auth/signin.html'
	context = {}

	def get(self,request,*args,**kwargs):
		form = SignUpForm()
		self.context['form'] = form

		response = render(request,self.template_name,self.context)
		return response
	@transaction.atomic
	def post(self,request,*args,**kwargs):
		form = SignUpForm(request.POST)
		self.context['form'] = form
		if form.is_valid():
			form.save()
			email = form.cleaned_data['email']
			password = form.cleaned_data['password1']
			user = authenticate(email = email,password = password)
			if user:
				login(request,user)
				return redirect('home')

		response = render(request,self.template_name,self.context)
		return response
	
class Login(generic.View):
	template_name = 'auth/login.html'
	context = {}

	def get(self,request,*args,**kwargs):
		form = LoginForm()
		self.context['form'] = form
		return render(request,self.template_name,self.context)
	def post(self,request,*args,**kwargs):
		form = LoginForm(request.POST)
		if form.is_valid():
			user = authenticate(email = form.cleaned_data['email'],
				password = form.cleaned_data['password'])
			if user:
				login(request,user)
				return redirect('home')
		return render(request,self.template_name,self.context)
		

