from django.urls import path
from . import views

urlpatterns = [
    path('', views.home , name = "home"),
    path('markAttendance', views.markAttendance , name = "markAttendance"),
    path('markLeave', views.markLeave , name = "markLeave"),
    path('viewAttendance', views.viewAttendance , name = "viewAttendance"),
    path('adminPanel', views.adminPanel , name = "adminPanel"),

]