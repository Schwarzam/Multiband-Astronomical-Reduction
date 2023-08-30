"""marServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from files.views import *
from files.query import rawQuery
from files.query import get_trilogy_image
from process.thread import get_logs

from django.shortcuts import render

from django.conf import settings
from django.conf.urls.static import static

from process.blockHandlers import *
from process.views import get_queue, remove_queue, get_conf, set_item_conf, get_operations, get_operations_stats, set_conf

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer

from django.http import HttpResponse

@api_view(["GET"])
@renderer_classes([JSONRenderer])
def media_access(request, path):
    response = HttpResponse(status=200)
    response['Content-Type'] = ''
    response['X-Accel-Redirect'] = '/reductionmedia/' + path
    return response

urlpatterns = [
    path('', include('accounts.urls')),

    path('reduction/individualfile', individualfile, name ='individualfile'),
    path('reduction/biasblock', biasblock, name ='biasblock'),
    path('reduction/finaltiles', finaltiles, name ='finaltiles'),
    path('reduction/flatblock', flatblock, name ='flatblock'),
    path('reduction/flatbyfilter', flatbyfilter, name ='flatbyfilter'),
    path('reduction/sciblock', sciblock, name ='sciblock'),
    path('reduction/scibyfilter', scibyfilter, name ='scibyfilter'),
    path('reduction/superflat', superflatblock, name='superflatblock'),

    path('reduction/fieldimages', fieldimages, name = 'fieldimages'),
    path('reduction/get_process', get_process, name ='get_process'),
    path('reduction/get_logs', get_logs, name ='get_logs'),
    path('reduction/clear_logs', clear_logs, name ='clear_logs'),
    path('reduction/scan_folder', scanfolder, name ='scan_folder'),
    path('reduction/reset_threads', reset_threads, name ='reset_threads'),

    path('reduction/get_queue', get_queue, name ='get_queue'),
    path('reduction/removeQueue', remove_queue, name ='removeQueue'),
    path('reduction/getConf', get_conf, name ='getConf'),
    path('reduction/setItemConf', set_item_conf, name ='setItemConf'),
    path('reduction/set_conf', set_conf, name ='set_conf'),

    path('reduction/getOperations', get_operations, name ='getOperations'),

    path('reduction/rawQuery', rawQuery, name ='rawQuery'),
    path('reduction/getOperationsStats', get_operations_stats, name ='get_operations_stats'),

    path('reduction/get_trilogy_image', get_trilogy_image, name ='get_trilogy_image'),
    path('reduction/request_twelve_im', request_twelve_band_im, name ='request_twelve_band_im'),

    path('reduction/admin', admin.site.urls),
    re_path(r'^media/(?P<path>.*)', media_access, name='media'),
] 
