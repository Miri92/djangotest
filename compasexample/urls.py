"""compasexample URL Configuration

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
from django.urls import path, include
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.welcome, name='welcome'),
    path('user/profile', views.index, name='profile'),
    path('user/', include('user_example.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('addTodo', views.addTodo),
    path('todo/update/<int:id>', views.update, name='updateTodo'),
    path('todo/delete/<int:id>', views.delete, name='deleteTodo'),
    path('todo/delete/<int:id>', views.delete, name='deleteTodo'),
    path('todo/detail/<int:id>', views.detail, name='detailTodo'),


    path('todo/share', views.share_todo, name='shareTodo'),
]
