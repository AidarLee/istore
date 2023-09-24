from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path('profile', views.profile, name='profile'),
    path('login', views.login_user, name='login'),
    path('login_google', views.login_google, name='login_google'),
    path('login_google_resp', views.login_google_resp, name='login_google_resp'),
    path('login_facebook', views.login_facebook, name='login_facebook'),
    path('login_facebook_resp', views.login_facebook_resp,
         name='login_facebook_resp'),
    path('login_apple_resp', views.login_apple_resp,
         name='login_apple_resp'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register, name='register'),
    path('edit', views.edit, name='edit'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('forget', views.forget, name='forget'),
    path('forget_modal', views.forget_modal, name='forget_modal'),
    path('set_code', views.set_code, name='set_code'),
    path('get_code_time', views.get_code_time, name='get_code_time'),
    path('check_code', views.check_code, name='check_code'),
    path('save_avatar', views.save_avatar, name='save_avatar'),
    path('remove_avatar', views.remove_avatar, name='remove_avatar'),
]
