"""
URL configuration for IT_company_task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib.auth import views as auth_views

from tasks.forms import LoginForm
from tasks.views import WorkerRegisterView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("tasks.urls", namespace="tasks")),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            form_class=LoginForm,
            template_name="registration/login.html",
        ),
        name="login",
    ),
    path("accounts/register/", WorkerRegisterView.as_view(), name="register"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
else:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
