from django.urls import path

from hongtingapp.views import match_profiles, perform_matching, perform_info_matching

urlpatterns = [
    path('matching/', match_profiles, name='matching'),

    path('YouInfo/', perform_info_matching, name='YouInfo'),

]
