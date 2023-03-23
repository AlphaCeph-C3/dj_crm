"""djcrm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import include, path

from crm.views import LandingPageView, SignupView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", LandingPageView.as_view(), name="landing-page"),
    path("leads/", include("crm.urls", namespace="crm")),
    path("agents/", include("agents.urls", namespace="agents")),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(redirect_authenticated_user=True), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("reset_password/", PasswordResetView.as_view(), name="reset_password"),
    path(
        "password_reset_done/",
        PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
