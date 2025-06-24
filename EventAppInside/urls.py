from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/',views.signup, name ='signup'),
    path('login/', views.login, name='login'),
    path('front/', views.front_page, name="front"),
    path('set-event-type/', views.set_event_type, name="set_event_type"), 
    path('location/', views.location, name="location"),
    path("timeline/", views.timeLineEvents, name="timeLineEvents"),
    path("posts/", views.posts, name="posts"),
    #path("post/<int:post_id>/", views.post_detail, name="post_detail"),
    #path("post/<int:post_id>/like/", views.toggle_like, name="toggle_like"),
    #path("post/<int:post_id>/comment/", views.add_comment, name="add_comment"),
    path("upload/", views.upload_post, name="upload_post"),
    path("save-post/", views.save_post, name="save_post"),
    path("admin_login/", views.admin_login, name="admin_login"),
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),
     path('select_photo/', views.select_photo, name='select_photo'),
     path('post_detail/', views.post_detail, name="post_detail"),

]