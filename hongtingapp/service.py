from .models import UserProfile

class UserProfileService:
    @staticmethod
    def create_user_profile(profile_data):
        user_profile = UserProfile.objects.create(**profile_data)
        return user_profile
