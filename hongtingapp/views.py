from django.shortcuts import render
from django.db.models import Q
from .models import UserProfile, Info
from .service import UserProfileService



#소개팅에서 항목별로 값을 리스트로 받았을 때의 매칭 알고리즘
def match_profiles(category01, values01, category02, values02, user_gender):
    q1 = Q()
    q2 = Q()


    #user_gender 값과 반대 성별인 상대방 중에서만 검사하도록 조건 부여
    if user_gender == 'M':
        q1 &= Q(gender='F')
    elif user_gender == 'F':
        q1 &= Q(gender='M')

    # 여자일 때에만 군필 여부 검사
    #if user_gender == 'F':
        #q1 &= Q(army__in=['군필', '면제'])

    #첫 번째 항목의 값과 일치하는 프로필을 모두 q1객체에 저장
    for value in values01:
        if category01 == 'mbti':
            q1 |= Q(mbti=value)
        elif category01 == 'height':
            q1 |= Q(height=value)
        elif category01 == 'age':
            q1 |= Q(age=value)
        elif category01 == 'body':
            q1 |= Q(body_face=value)
        elif category01 == 'eyes':
            q1 |= Q(eyes=value)
        elif category01 == 'hobby':
            q1 |= Q(hobby=value)
        else:
            q1 |= Q(major=value)


    #두 번째 항목의 값과 일치하는 프로필을 모두 q2객체에 저장
    for value in values02:
        if category02 == 'mbti':
            q2 |= Q(mbti=value)
        elif category02 == 'height':
            q2 |= Q(height=value)
        elif category02 == 'age':
            q2 |= Q(age=value)
        elif category02 == 'body':
            q2 |= Q(body=value)
        elif category02 == 'eyes':
            q2 |= Q(eyes=value)
        elif category02 == 'hobby':
            q2 |= Q(hobby=value)
        else:
            q2 |= Q(major=value)



    #첫 번째 항목의 값과 두 번째 항목의 값이 모두 일치하는 프로필을 모두 matches 에 저장
    matches = UserProfile.objects.filter(q1 & q2)
    return matches

#미팅에서 항목 별로 값을 리스트로 받았을 때의 매칭 알고리즘
def match_info_profiles(category01, values01, category02, values02, user_gender, peoplenums):
    # 상대방 성별과 맞지 않는 경우만 필터링
    gender_filter = ~Q(gender=user_gender)

    # 미팅 인원 수는 무조건 일치해야 함
    peoplenums_filter = Q(peoplenums=peoplenums)

    # 첫 번째 항목의 값과 일치하는 프로필 필터
    values01_filter = Q()
    for value in values01:
        if category01 == 'jobs':
            values01_filter |= Q(jobs=value)
        elif category01 == 'locations':
            values01_filter |= Q(locations=value)
        else:
            values01_filter |= Q(ages=value)

    # 두 번째 항목의 값과 일치하는 프로필 필터
    values02_filter = Q()
    for value in values02:
        if category02 == 'jobs':
            values02_filter |= Q(jobs=value)
        elif category02 == 'locations':
            values02_filter |= Q(locations=value)
        else:
            values02_filter |= Q(ages=value)

    # 모든 필터를 조합하여 결과를 가져옴
    info_matches = Info.objects.filter(gender_filter & peoplenums_filter & values01_filter & values02_filter)

    return info_matches






#소개팅 매칭 함수
def perform_matching(request):

    #임의로 만든 사용자가 선택한 항목과 값 -> category01, category02는 항목, values01, values02는 항목의 값
    category01 = 'mbti'
    values01 = ['esfp', 'entp']
    category02 = 'body'
    values02 = ['마름', '두부', '뚜렷']
    user_gender = 'M'


    #소개팅 알고리즘 돌린 후 조건에 맞는 프로필을 모두 matched_profiles_both 에 저장
    matched_profiles = match_profiles(category01, values01, category02, values02, user_gender)




    return render(request, 'YouInfo.html', {'matched_profiles': matched_profiles})


#미팅 매칭 함수
def perform_info_matching(request):
    # 임의로 만든 사용자가 선택한 항목과 값
    category01 = 'jobs'
    values01 = ['student', '대학원생']
    category02 = 'ages'
    values02 = ['21', '22', '23', '24', '25', '26', '27', '28', '29']
    user_gender = 'F'
    peoplenums = '2'
    # 미팅 알고리즘을 돌린 후 조건에 맞는 프로필을 모두 matched_info_both 에 저장
    matched_info = match_info_profiles(category01, values01, category02, values02, user_gender, peoplenums)



    return render(request, 'YouInfo.html', {'matched_profiles': matched_info})

#카카오톡 아이디를 고유 값으로 받아 정보 분리해서 저장