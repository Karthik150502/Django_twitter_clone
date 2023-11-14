from django.urls import path
from juneapp import views

urlpatterns = [
    path("",views.home, name = "home"),
    path("profile_list", views.profile_list, name = "profile_list"),
    path("profile/<int:pk>", views.profile, name="profile"),
    path("profile/followers_page/<int:pk>", views.followers_page, name = "followers_page"),
    path("profile/following_page/<int:pk>", views.following_page, name = "following_page"),
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("register", views.register, name="register"),
    path("update_user", views.update_user, name="update_user"),
    path("june_like/<int:pk>", views.june_like, name = "june_like"),
    path("june_share/<int:pk>", views.june_share, name = "june_share"),
    path("unfollow/<int:pk>", views.unfollow, name = "unfollow"),
    path("follow/<int:pk>", views.follow, name = "follow"),
    path("delete_june/<int:pk>", views.delete_june, name = "delete_june"),
    path("edit_june/<int:pk>", views.edit_june, name = "edit_june"),
    path("search_june", views.search_june, name="search_june"),
    path("search_user", views.search_user, name="search_user"),
]
