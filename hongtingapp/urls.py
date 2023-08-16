from django.urls import path

from hongtingapp.views import create_user_profile, match_profiles, perform_matching

urlpatterns = [
    path('matching/', match_profiles, name='matching'),
    path('home/', create_user_profile, name='home'),
    path('YouInfo/', perform_matching, name='YouInfo'),

]
