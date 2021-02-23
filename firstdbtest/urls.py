from django.urls import path, include
from django.conf.urls import url

from firstdbtest import views

urlpatterns = [
   # path('', views.index, name='index'),
    url(r'^addstudentinfo/$', views.addstudentinfo),
    # url(r'^delstudentinfo/$', views.delstudentinfo),
    url(r'^getstudentinfo/$', views.getstudentinfo),
    url(r'^addsuccess/$', views.addsuccess),
    path('students/', views.StudentListView.as_view(), name = 'students'),
]
