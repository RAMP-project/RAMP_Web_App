"""ramp_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls.i18n import i18n_patterns
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from users import views as users_views
from django.conf import settings
from django.conf.urls.static import static
from main import views as main_views

# Browsers search for favicon.ico in the root directory, Django prefers it in the static folder.
# So this redirects browser requests to the static folder.
urlpatterns = [
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
    path('i18n/', include('django.conf.urls.i18n')),
]


urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include("main.urls")),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', users_views.logout_view, name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(success_url='/profile', extra_context={'success_message': "You were successfully logged in"}), name="password_change"),
    path('register/', users_views.register, name='register-users'),
    path('profile/', users_views.profile, name='profile'),
    path('delete_account', users_views.delete_account, name="delete_account"),
    prefix_default_language=True,
)
