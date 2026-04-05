from django.urls import path
from .views import *

app_name = 'user'

urlpatterns = [
    # Auth
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='sign_in'),
    path('logout/', UserLogoutView.as_view(), name='sign_out'),
    path('auth/google/callback/', google_login_callback, name='google_callback'),

    path('profile/<str:username>/', ProfileDetailView.as_view(), name="profile_detail"),
    path('edit-profile/', ProfileUpdateView.as_view(), name="profile_update"),
    path('delete-profile/', ProfileDeleteView.as_view(), name="profile_delete"),

    path('follow_user/<str:username>/', follow_toggle, name="follow_user"),
    path('profile/<str:username>/following/', user_following_list, name="user_following"),
    path('profile/<str:username>/followers/', user_followers_list, name='user_followers'),
]
