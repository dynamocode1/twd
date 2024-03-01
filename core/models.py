from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
import uuid
#from mezzanine.core.fields import RichTextField
from ckeditor.fields import RichTextField
from django.urls import reverse_lazy
import uuid
class UserManager(BaseUserManager):
	def create_user(self,email = None,password = None,**extra_field):
		if email == None:
			raise ValueError('Email Is Needed')
		user = self.model(email = email)
		user.set_password(password)
		user.save(using = self._db)
		return user

	def create_superuser(self,email,password,**extra_field):
		user = self.create_user(email,password,**extra_field)
		extra_field.setdefault('is_staff',True)
		extra_field.setdefault('is_superuser',True)
		return user

class User(AbstractBaseUser,PermissionsMixin):
	id = models.UUIDField(primary_key = True,editable = False,default = uuid.uuid4,unique = True)
	username = models.CharField(max_length = 340)
	email = models.EmailField(unique = True)
	lname = models.CharField(max_length= 65)
	fname = models.CharField(max_length = 65)
	date = models.DateField(auto_now_add = True)
	is_active = models.BooleanField(default = True)
	is_staff = models.BooleanField(default = False)
	is_superuser = models.BooleanField(default = False)
	verified = models.BooleanField(default = False)
	objects = UserManager()
	USERNAME_FIELD = 'email'

	def __str__(self):
		return self.email 
class CourseCategory(models.Model):
	name = models.CharField(max_length = 120)
class Course(models.Model):
	id  = models.UUIDField(default = uuid.uuid4,primary_key = True)
	
	category = models.ForeignKey(CourseCategory,related_name = 'courses',on_delete = models.CASCADE,null = True,blank = True)
	date = models.DateField(auto_now_add = True)
	image = models.URLField()
	title = models.CharField(max_length = 120)
	description = models.TextField()
	pub = models.BooleanField(default = False)

	def get_url(self):
		return reverse_lazy('view_course',kwargs = {'course_id':self.id})

	def get_topics(self):
		return reverse_lazy('view_topics',kwargs = {'topic_id':self.id})

	@property
	def is_pub(self):
		return self.pub
	

class Topic(models.Model):
	course = models.ForeignKey('Course',on_delete = models.CASCADE,related_name = 'topics')
	title = models.CharField(max_length = 120)
	date = models.DateField(auto_now_add = True)
	body = 	RichTextField()
	pub = models.BooleanField(default = False)

class Blog(models.Model):
	id  = models.UUIDField(default = uuid.uuid4,primary_key = True)
	title = models.CharField(max_length = 506)
	body = RichTextField()
	date = models.DateTimeField(auto_now_add = True)
	image = models.URLField(blank = True,null = True)

	def __str__(self):
		return self.title

class Admin(models.Model):
	username = models.CharField(max_length = 50)
	password = models.CharField(max_length =  50)

	class Meta:
		db_table = 'admin'

	def __str__(self):
		return self.username

class PasswordResetToken(models.Model):
	id = models.UUIDField(default = uuid.uuid4,unique = True,primary_key = True)
	user = models.ForeignKey(User,on_delete = models.CASCADE)
	date = models.DateField(auto_now_add = True)
	used = models.BooleanField(default = False)

	def __str__(self):
		return self.id