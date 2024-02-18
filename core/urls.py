from django.urls import path
from .views import Home,Register,Courses,CoursesSearch,LearnCourse,About,Blogs,ReadBlog,Login
from .adminview import *
urlpatterns = [
path('',Home.as_view(),name = 'home'),
path('auth/register',Register.as_view(),name = 'register'),
path('auth/login',Login.as_view(),name = 'login'),
path('courses',Courses.as_view(),name = 'courses'),
path('courses/search',CoursesSearch.as_view(),name = 'courses_search'),
path('courses/<int:id>',LearnCourse.as_view(),name = 'course'),
path('about',About.as_view(),name = 'about'),
path('blogs',Blogs.as_view(),name = 'blogs'),
path('blogs/read_more/<int:pk>',ReadBlog.as_view(),name = 'read_blog')
]



admin_urls = [
path('cp/admin',AdminHome.as_view(),name = 'admin_home'),
path('cp/admin/courses/new',NewCourse.as_view(),name = 'new_course'),
path('cp/admin/courses/view/<int:course_id>',ViewCourse.as_view(),name = 'view_course'),
path('cp/admin/topics/<int:topic_id>',ViewTopics.as_view(),name = 'view_topics'),
path('cp/admin/topics/edit/<int:topic_id>',EditTopics.as_view(),name = 'edit_topic'),
path('cp/admin/topics/delete/<int:id>',delete_topic,name = 'delete_topic'),
path('cp/admin/courses/all',AllCourses.as_view(),name = 'all_course'),
path('cp/admin/courses/edit/<int:id>',EditCourse.as_view(),name = 'edit_course'),
path('cp/admin/courses/delete/<int:id>',delete_course,name = 'delete_course'),
path('cp/admin/blogs/new',NewBlog.as_view(),name = 'new_blog'),
path('cp/admin/blogs/all',AllBlog.as_view(),name = 'all_blog'),
path('cp/admin/blogs/delete/<int:id>',delete_blog,name = 'delete_blog'),
path('cp/admin/blogs/edit/<int:id>',EditBlog.as_view() ,name = 'edit_blog'),
path('cp/admin/courses/pub/<int:id>',PubCourse,name = 'pub'),
path('cp/admin/login',AdminLogin.as_view(),name = 'adminlogin'),
path('no_perm',no_perm,name = 'no_perm')
]

urlpatterns+=admin_urls