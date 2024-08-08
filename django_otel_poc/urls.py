"""
URL configuration for django_otel_poc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.urls import re_path
from django.views.static import serve
from .settings import STATIC_ROOT, STATIC_URL
from re import escape

urlpatterns = ([
        path('admin/', admin.site.urls),
        path('hcms/', include("hcms.urls")),
        re_path(r"^%s(?P<path>.*)$" % escape(STATIC_URL.lstrip("/")), serve, kwargs=dict(document_root=STATIC_ROOT))
    ]
)
