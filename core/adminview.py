from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import NewCourseForm,TopicForm,NewBlogForm,AdminLoginForm
from .models import Course,Topic,Blog,Admin,User
from .utils import admin_required
from django.utils.decorators import method_decorator
from .utils import authenticate_admin
from cloudinary.uploader import upload
from django.db import transaction
def no_perm(request):
	return render(request,'admin/no_perm.html')
@method_decorator(admin_required,name = 'dispatch')
class AdminHome(generic.TemplateView):
	template_name = 'admin/home.html'

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		courses = Course.objects.all()
		blogs = Blog.objects.all()
		users = User.objects.all()
		context['courses'] = courses
		context['blogs'] = blogs
		context['users'] = users

		return context
@method_decorator(admin_required,name = 'dispatch')
class NewCourse(generic.View):
	template_name = 'admin/newcourse.html'
	context = {}

	def get(self,request,*args,**kwargs):
		form = NewCourseForm()
		self.context['form'] = form
		resp = render(request,self.template_name,self.context)
		return resp

	def post(self,request,*args,**kwargs):
		form = NewCourseForm(request.POST,request.FILES)
		self.context['form'] = form
		if form.is_valid():
			cd = form.cleaned_data
			cloud = upload(cd['image']);image = cloud['url']
			course = Course.objects.create(title = cd['title'],description = cd['description'],image = image)
			course.save()
			return redirect('admin_home')
		else:
			form_error = form.errors
			print(form_error)
			resp = render(request,self.template_name,self.context)


		resp = render(request,self.template_name,self.context)
		return resp

@method_decorator(admin_required,name = 'dispatch')
class ViewCourse(generic.View):
	template_name = 'admin/newtopic.html'
	context = {}

	def get(self,request,course_id,*args,**kwargs):
		form = TopicForm()
		self.context['form'] = form
		self.context['topic'] = Course.objects.get(id = course_id).topics
		self.context['course'] = Course.objects.get(id = course_id)
		return render(request,self.template_name,self.context)
	def post(self,request,*args,**kwargs):
		form = TopicForm(request.POST)
		self.context['form'] = form
		if form.is_valid():
			cd = form.cleaned_data
			course = Course.objects.get(id = kwargs.get('course_id'))
			topic = Topic(course = course,title = cd['title'],body = cd['content'])
			topic.save()
			return redirect('admin_home')
		return render(request,self.template_name,self.context)
@method_decorator(admin_required,name = 'dispatch')
class ViewTopics(generic.View):
	template_name = 'admin/view_topics.html'
	context = {}
	def get(self,request,topic_id,*args,**kwargs):
		topics = Course.objects.get(id = topic_id).topics.all()
		self.context['topics'] = topics

		return render(request,self.template_name,self.context)
@method_decorator(admin_required,name = 'dispatch')
class EditTopics(generic.View):
	template_name = 'admin/edit_topics.html'
	context = {}

	def get(self,request,topic_id,*args,**kwargs):
		topic = Topic.objects.get(id = topic_id)
		initial_data = {'title':topic.title,'content':topic.body}
		form = TopicForm(initial = initial_data)
		self.context['form'] = form

		return render(request,self.template_name,self.context)
	def post(self,request,*args,**kwargs):
		topic = Topic.objects.get(id = kwargs.get('topic_id'))
		initial_data = {'title':topic.title,'content':topic.body}
		form = TopicForm(request.POST)
		self.context['form'] = form
		if form.is_valid():
			title = form.cleaned_data['title']
			body = form.cleaned_data['content']
			topic.title = title
			topic.body = body
			topic.save()
			url = reverse_lazy('view_topics',kwargs = {'topic_id':topic.id})
			return redirect('admin_home')
		return render(request,self.template_name,self.context)
@admin_required
def delete_topic(request,id):
	topic = Topic.objects.get(id = id)
	topic_id = topic.course.id
	topic.delete()
	url = reverse_lazy('view_topics',kwargs = {'topic_id':topic_id})
	return redirect(url)
@admin_required
def delete_course(request,id):
	course = Course.objects.get(id = id)
	course.delete()
	return redirect('all_course')
@admin_required
def delete_blog(request,id):
	course = Blog.objects.get(id = id)
	course.delete()
	return redirect('all_blog')
@method_decorator(admin_required,name = 'dispatch')
class AllCourses(generic.ListView):
	template_name = 'admin/all_courses.html'
	model = Course
	context_object_name = 'course'
	def get_queryset(self):
		qs = Course.objects.all()
		return qs 
@method_decorator(admin_required,name = 'dispatch')
class EditCourse(generic.View):
	template_name = 'admin/edit_courses.html'
	context = {}

	def get(self,request,id,*args,**kwargs):
		obj = Course.objects.get(id = id)
		form = NewCourseForm(instance = obj)
		self.context['form'] = form

		resp = render(request,self.template_name,self.context)
		return resp

	def post(self,request,*args,**kwargs):
		form = NewCourseForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			obj = Course.objects.get(id = kwargs.get('id'))
			obj.image = cd['image']
			obj.title = cd['title']
			obj.description = cd['description']
			obj.save()

			return redirect('all_course')
		resp = render(request,self.template_name,self.context)

		return resp
@method_decorator(admin_required,name = 'dispatch')
class NewBlog(generic.View):
	template_name = 'admin/new_blog.html'
	context = {}

	def get(self,request,*args,**kwargs):
		form = NewBlogForm()
		self.context['form'] = form
		return render(request,self.template_name,self.context)
	def post(self,request,*args,**kwargs):
		form = NewBlogForm(request.POST,request.FILES)
		self.context['form'] = form
		if form.is_valid():
			cd = form.cleaned_data
			cloud = upload(cd['image'])
			blog  = Blog.objects.create(title = cd['title'],body = cd['body'],image = cloud['url']) 
			blog.save()
			return redirect('admin_home')
		return render(request,self.template_name,self.context)



@method_decorator(admin_required,name = 'dispatch')
class AllBlog(generic.ListView):
	template_name = 'admin/all_blogs.html'
	model = Blog
	context_object_name = 'blogs'
	def get_queryset(self):
		return Blog.objects.all()
@method_decorator(admin_required,name = 'dispatch')
class EditBlog(generic.View):
	template_name = 'admin/edit_blogs.html'
	context = {}

	def get(self,request,id,*args,**kwargs):
		obj = Blog.objects.get(id = id)
		obj = {'title':obj.title,'body':obj.body}
		form = NewBlogForm(initial = obj)
		self.context['form'] = form

		resp = render(request,self.template_name,self.context)
		return resp

	def post(self,request,*args,**kwargs):
		form = NewBlogForm(request.POST,request.FILES)
		if form.is_valid():
			cd = form.cleaned_data
			obj = Blog.objects.get(id = kwargs.get('id'))
			obj.image = cd['image']
			obj.title = cd['title']
			obj.body = cd['body']
			obj.save()

			return redirect('all_blog')
		resp = render(request,self.template_name,self.context)

		return resp
@admin_required
def PubCourse(request,id):
	instance = Course.objects.get(id = id)
	if instance.is_pub:
		instance.pub = False
		instance.save()
		return redirect('all_course')
	else:
		instance.pub = True
		instance.save()
		print('NoT Published')
		return redirect('all_course')

class AdminLogin(generic.View):
	template_name = 'admin/login.html'
	context = {}
	def get(self,request,*args,**kwargs):
		form = AdminLoginForm()
		self.context['form'] = form

		return render(request,self.template_name,self.context)

	def post(self,request,*args,**kwargs):
		form = AdminLoginForm(request.POST)
		if form.is_valid():
			instance = Admin.objects.get(username = form.cleaned_data['username'])
			if instance:
				if instance.password == form.cleaned_data['password']:
					response = redirect('admin_home')
					session_id = authenticate_admin(request)
					response.set_cookie('admin_id',session_id)
					return response
				else:
					print('wrong password')
					return redirect('adminlogin')

			else:
				print('wrong username')
				return redirect('adminlogin')
		self.context['form']  = form
		return redirect('adminlogin')