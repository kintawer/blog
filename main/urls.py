"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from .views import Index, About, Contact, Post, Subscribe, Comment

urlpatterns = [
    path('', Index.as_view()),
    path('about/', About.as_view(), name='about'),
    path('contact/', Contact.as_view(), name='contact'),
    path('post/<slug:slug>', Post.as_view(), name='post'),
    path('subscribe/', Subscribe.as_view(), name='subscribe'),
    path('comment/', Comment.as_view(), name='comment'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
