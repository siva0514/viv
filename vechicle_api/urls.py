"""vechicle_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
import api.views

urlpatterns = [
    path('', api.views.index),
    path('video_index/', api.views.video_index),
    path('api/vehicle/eur/', api.views.get_details),
    path('api/vehicle_list/', api.views.vehicle_list),
    path('api/process_video/', api.views.process_video, name='process_video'),
    path('api/webcam_video/', api.views.webcam_video, name='webcam_video'),
]
