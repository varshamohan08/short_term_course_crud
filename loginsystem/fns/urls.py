from django.urls import path, include
from .views import *

urlpatterns = [
    path('fns', UserActions.as_view(), name='reg'),
    path('login', userLogin.as_view(), name='login'),
    path('logout', userLogout.as_view(), name='logout'),
    path('short_course', ShortCourseAPI.as_view(), name='short_course'),
    path('short_course/<int:id>', ShortCourseAPI.as_view(), name='short_course'),
    path('add_short_course', AddShortCourseAPI.as_view(), name='add_short_course'),
    path('update_short_course/<int:id>', UpdateShortCourseAPI.as_view(), name='update_short_course'),
    path('user_profile', userProfile.as_view(), name='user_profile'),
]
