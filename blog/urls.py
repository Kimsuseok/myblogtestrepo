
from django.conf.urls import url
from . import views

app_name = 'blog'

urlpatterns = [
    url(r'^write/$', views.post_write, name='write'),
    url(r'^write/upload/$', views.fileupload, name='upload'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.post_edit, name='edit'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.post_delete, name='delete'),
    url(r'^(?P<pk>[0-9]+)/$', views.post_detail, name='detail'),
    url(r'^list/$', views.post_list, name='list'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^$', views.index, name='index'),
]

#TODO
"""
    url(r'^category/(?P<pk>[.*]+)/$', views.aaa, name='category'),
    url(r'^tag/[.*]+', views.aaa, name='tag'),  # 뒤에 오는 path가 여러개 올수있도록..?
    url(r'^archive/(?P<date>[.*]+)/&', views.aaa, name='archive'),  # 날짜 정규식으로 바꿔야..
"""
