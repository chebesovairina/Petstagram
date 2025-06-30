from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/', views.my_profile, name='my_profile'),
    path('feed/', views.feed, name='feed'),
    path('create-post/', views.create_post, name='create_post'),
    path('posts/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('posts/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('toggle_follow/<int:user_id>/', views.toggle_follow, name='toggle_follow'),
    path('feed/following/', views.following_feed, name='following_feed'),
]