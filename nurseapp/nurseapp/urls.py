"""nurseapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path

from nurseapp import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^patient/delete$', views.patient_delete, name='patient_delete'),
    url(r'^patient/add$', views.patient_add, name='patient_add'),
    url(r'^patient/check', views.patient_check, name='patient_check'),
    path('patient/view/<int:patient_id>', views.patient_view, name='patient_view'),
    path('patient/edit/<int:patient_id>', views.patient_edit, name='patient_edit'),
]
