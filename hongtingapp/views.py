from django.shortcuts import render
from django.db.models import Q
from .models import UserProfile
from .service import UserProfileService

def create_user_profile(request):
    if request.method == 'POST':
        age = request.POST.get('age')
        gender = request.POST.get('sex')
        group_size = request.POST.get('group_size')
        major = request.POST.get('major')
        mbti = request.POST.get('mbti')
        army = request.POST.get('army')
        height = request.POST.get('height')
        body_face = request.POST.get('type')
        eyes = request.POST.get('eyes')
        hobby = request.POST.get('hobby')
        self_intro = request.POST.get('self_intro')

        profile_data = {
            'age': age,
            'gender': gender,
            'group_size': group_size,
            'major': major,
            'mbti': mbti,
            'army': army,
            'height': height,
            'body_face': body_face,
            'eyes': eyes,
            'hobby': hobby,
            'self_intro': self_intro,
        }

        user_profile = UserProfileService.create_user_profile(profile_data)
        return render(request, 'home.html', {'user_profile': user_profile})

    return render(request, 'matching.html')





#항목별로 값을 리스트로 받았을 때의 매칭 알고리즘
def match_profiles(selected_category01, selected_values01, selected_category02, selected_values02):
    q1 = Q()
    q2 = Q()


#첫 번째 선택 항목에 맞는 프로필 필터링 후 q1객체에 저장
    for value in selected_values01:
        if selected_category01 == 'mbti':
            q1 |= Q(mbti=value)
        elif selected_category01 == 'height':
            q1 |= Q(height=value)
        elif selected_category01 == 'age':
            q1 |= Q(age=value)
        elif selected_category01 == 'body_face':
            q1 |= Q(body_face=value)
        elif selected_category01 == 'eyes':
            q1 |= Q(eyes=value)
        elif selected_category01 == 'army':
            q1 |= Q(army=value)
        elif selected_category01 == 'hobby':
            q1 |= Q(hobby=value)
        else:
            q1 |= Q(major=value)


#두 번째 선택 항목에 맞는 프로필 필터링 후 q2객체에 저장
    for value in selected_values02:
        if selected_category02 == 'mbti':
            q2 |= Q(mbti=value)
        elif selected_category02 == 'height':
            q2 |= Q(height=value)
        elif selected_category02 == 'age':
            q2 |= Q(age=value)
        elif selected_category02 == 'body_face':
            q2 |= Q(body_face=value)
        elif selected_category02 == 'eyes':
            q2 |= Q(eyes=value)
        elif selected_category02 == 'army':
            q2 |= Q(army=value)
        elif selected_category02 == 'hobby':
            q2 |= Q(hobby=value)
        else:
            q2 |= Q(major=value)


#matches 에 q1객체와 q1객체 모두에 포함된 프로필 필터링 후 저장
    matches = UserProfile.objects.filter(q1 & q2)
    return matches


def perform_matching(request):
    # 임의의 선택 값을 사용하여 매칭 수행 예시
    selected_category01 = 'age'
    selected_values01 = ['a', 'b']
    selected_category02 = 'mbti'
    selected_values02 = ['a']

    matched_profiles = match_profiles(selected_category01, selected_values01, selected_category02, selected_values02)

    return render(request, 'YouInfo.html', {'matched_profiles': matched_profiles})