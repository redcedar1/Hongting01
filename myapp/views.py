import ast

from allauth.socialaccount.models import SocialAccount
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Info
from myproject import settings
import requests
from django.template import loader
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden

# Create your views here.
  
count = 0
@csrf_exempt
def index(request):
   return redirect("/home")



def kakaologin(request):
    context = {'check': False}
    if request.session.get('access_token'):
        access_token = request.session.get('access_token')
        account_info = requests.get("https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"}).json()
        kakao_id = account_info.get("id")
        print("kakao_id : ", kakao_id)
        try:
            user_profile = Info.objects.get(kakao_id=kakao_id)  # 카카오톡 ID를 사용하여 사용자 정보 조회
            context['user_profile'] = user_profile
        except Info.DoesNotExist:
            # 새로운 레코드 생성
            user_profile = Info(kakao_id=kakao_id)
            user_profile.save()
            context['user_profile'] = user_profile

        return redirect("/home") #로그인 되어있으면 home페이지로

    return render(request, "myapp/kakaologin.html", context)

def kakaoLoginLogic(request):
    _restApiKey = '60010e5242c371826d538b43def648c3' # 입력필요
    _redirectUrl = 'http://127.0.0.1:8000/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/authorize?client_id={_restApiKey}&redirect_uri={_redirectUrl}&response_type=code'
    return redirect(_url)

def kakaoLoginLogicRedirect(request):
    _qs = request.GET['code']
    _restApiKey = '60010e5242c371826d538b43def648c3' # 입력필요
    _redirect_uri = 'http://127.0.0.1:8000/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={_restApiKey}&redirect_uri={_redirect_uri}&code={_qs}'
    _res = requests.post(_url)
    _result = _res.json()
    print()
    print(_result)
    print()
    request.session['access_token'] = _result['access_token']
    request.session.modified = True

    return redirect("/home") #로그인 완료 후엔 home페이지로


def kakaoLogout(request):
    _token = request.session['access_token']
    _url = 'https://kapi.kakao.com/v1/user/logout'
    _header = {
        'Authorization': f'bearer {_token}'
    }
    _res = requests.post(_url, headers=_header)
    _result = _res.json()

    print(_result.get('id'))  # 액세스 토큰은 바뀌어도 id값은 안바뀌니 이것으로 조회 가능
    if _result.get('id'):

        del request.session['access_token']
        return render(request, 'myapp/loginoutsuccess.html')
    else:
        return render(request, 'myapp/logouterror.html')


@csrf_exempt
def home(request):
    logged = 0

    access_token = request.session.get("access_token", None)
    if access_token:
        logged = 1

    context = {'logged': logged}
    return render(request, "myapp/home.html", context)

@csrf_exempt
def meeting(request):
    access_token = request.session.get("access_token", None)
    if access_token == None:  # 로그인 안돼있으면
        return render(request, "myapp/kakaologin.html")  # 로그인 시키기

    account_info = requests.get("https://kapi.kakao.com/v2/user/me",
                                headers={"Authorization": f"Bearer {access_token}"}).json()
    global count
    if request.method == "POST":
        peoplenum = request.POST.getlist('submit_peoplenum')
        avgage = request.POST.get('submit_age')  # 평균 연령 정보 추출

        if not peoplenum:  # 인원 값이 없을 경우
            errormsg = {"error_message": "인원을 선택하지 않으셨습니다."}
            return render(request, "myapp/meeting.html", errormsg)

        # 현재 로그인한 사용자의 kakao_id 가져오기
        kakao_id = account_info.get("id")
        print("kakao_id : ", kakao_id)

        # 해당 kakao_id를 가진 사용자 정보 가져오기
        user_info = get_object_or_404(Info, kakao_id=kakao_id)

        # peoplenum과 avgage 정보 업데이트
        user_info.peoplenum = ', '.join(peoplenum)  # 리스트를 문자열로 변환하여 저장
        user_info.avgage = avgage
        user_info.save()

        count = user_info.id
        print(count)
        return redirect("/meeting2")  # /home/meeting2로 페이지 전달

    return render(request, "myapp/meeting.html")


@csrf_exempt
def meeting2(request):
    access_token = request.session.get("access_token", None)
    if access_token == None:  # 로그인 안돼있으면
        return render(request, "myapp/kakaologin.html")  # 로그인 시키기

    account_info = requests.get("https://kapi.kakao.com/v2/user/me",
                                headers={"Authorization": f"Bearer {access_token}"}).json()

    global count
    if request.method == "POST":
        jobs = request.POST.getlist('submit_job')
        age_values = request.POST.getlist('submit_age')

        if not jobs:
            errormsg = {"error_message": "직업을 선택해 주세요."}
            return render(request, "myapp/meeting2.html", errormsg)
        kakao_id = account_info.get("id")
        print("kakao_id : ", kakao_id)

        user_info = get_object_or_404(Info, kakao_id=kakao_id)

        user_info.jobs = ', '.join(jobs)
        user_info.ages = ', '.join(age_values)  # 여러 개의 연령대 값을 하나의 문자열로 저장
        user_info.save()

        return redirect("/matching/")

    count += 1
    return render(request, "myapp/meeting2.html")
@csrf_exempt
def alonechoose(request):

    return render(request, "myapp/alonechoose.html")
@csrf_exempt
def alonechoose2(request):

    return render(request, "myapp/alonechoose2.html")
@csrf_exempt
def army(request):

    return render(request, "myapp/army.html")
@csrf_exempt
def body(request):

    return render(request, "myapp/body.html")
@csrf_exempt
def eyes(request):

    return render(request, "myapp/eyes.html")
@csrf_exempt
def height(request):

    return render(request, "myapp/height.html")
@csrf_exempt
def hobby(request):

    return render(request, "myapp/hobby.html")
@csrf_exempt
def kakao(request):
    access_token = request.session.get("access_token", None)
    if access_token == None:  # 로그인 안돼있으면
        return render(request, "myapp/kakaologin.html")  # 로그인 시키기

    account_info = requests.get("https://kapi.kakao.com/v2/user/me",
                                headers={"Authorization": f"Bearer {access_token}"}).json()
    email = account_info.get("kakao_account", {}).get("email")  # email이 있으면 email반환 없으면 빈칸 반환
    nickname = account_info.get("kakao_account", {}).get("nickname")

    return render(request, "myapp/kakao.html", {'nickname': nickname})
@csrf_exempt
def major(request):

    return render(request, "myapp/major.html")
@csrf_exempt
def mbti(request):

    return render(request, "myapp/mbti.html")

myinfo = {}


@csrf_exempt
def myinfo(request):
    access_token = request.session.get("access_token", None)
    if access_token == None:  # 로그인 안돼있으면
        return render(request, "myapp/kakaologin.html")  # 로그인 시키기

    account_info = requests.get("https://kapi.kakao.com/v2/user/me",
                                headers={"Authorization": f"Bearer {access_token}"}).json()
    email = account_info.get("kakao_account", {}).get("email")  # email이 있으면 email반환 없으면 빈칸 반환
    nickname = account_info.get("kakao_account", {}).get("nickname")
    # kakao_id를 이용해 사용자 정보 가져오기
    kakao_id = account_info.get("id")
    print("kakao_id : ", kakao_id)

    user_profile = get_object_or_404(Info, kakao_id=kakao_id)#kakao_id 안받아짐

    context = {
        'email': email,
        'nickname': nickname,
        'user_profile': user_profile,  # 사용자 정보를 context에 추가
    }

    return render(request, "myapp/myinfo.html", context)
@csrf_exempt
def success(request):

    return render(request, "myapp/success.html")
@csrf_exempt
def youinfo(request):

    return render(request, "myapp/youinfo.html")

def is_valid_transition(current_page, requested_page):
    # 요청한 페이지가 현재 페이지에서의 올바른 다음 페이지인지 확인
    requested_page_int = int(requested_page)
    if requested_page_int == current_page + 1 or current_page == requested_page_int :
        return True
    return False

@csrf_exempt
def my(request, id):
    access_token = request.session.get("access_token", None)
    if access_token == None:  # 로그인 안돼있으면
        return render(request, "myapp/kakaologin.html")  # 로그인 시키기
    account_info = requests.get("https://kapi.kakao.com/v2/user/me",
                                headers={"Authorization": f"Bearer {access_token}"}).json()

    kakao_id = account_info.get("id")
    print("kakao_id : ", kakao_id)

    if request.method == "GET":
        if int(id) == 1:
            if request.session.get('current_page'):
                del request.session['current_page']

        current_page = request.session.get('current_page', 0)
        if int(id) < current_page:
            current_page = int(id)

        if not is_valid_transition(current_page, id):
            # 올바른 페이지 이동이 아니면 거부
            return HttpResponseForbidden("Forbidden")

        # 페이지 이동을 허용하고, 세션 업데이트
        request.session['current_page'] = int(id)

    # 자기소개 한거 있으면 자기소개 내용 불러오고 choose페이지로 넘어가게
    global myinfo
    index = int(id)

    if request.method == "POST":
        if index == 1:
            request.session['age'] = request.POST.get("age")
        elif index == 2:
            request.session['sex'] = request.POST.get("sex")
        elif index == 3:
            request.session['job'] = request.POST.get("job")
        elif index == 4:
            request.session['school'] = request.POST.get("school")
            request.session['major'] = request.POST.get("major")
        elif index == 5:
            request.session['mbti'] = request.POST.get("mbti")
        elif index == 6:
            request.session['army'] = request.POST.get("army")
        elif index == 7:
            request.session['height'] = request.POST.get("height")
        elif index == 8:
            request.session['body'] = request.POST.get("body")
        elif index == 9:
            request.session['eyes'] = request.POST.get("eyes")
        elif index == 10:
            request.session['face'] = request.POST.get("face")
        elif index == 11:
            # hobby 필드는 복수 선택 가능이므로 리스트로 저장
            hobby_list = request.POST.getlist("hobby")
        else:
            index = 1

        index2 = index + 1
        if index2 > 11:  # 모든 정보를 입력한 경우
            # 세션에 저장된 정보를 하나의 Info 객체에 저장하고 세션 초기화
            myinfo = Info.objects.create(

                kakao_id=kakao_id,
                age=request.session.get('age'),
                sex=request.session.get('sex'),
                job=request.session.get('job'),
                school=request.session.get('school'),
                major=request.session.get('major'),
                mbti=request.session.get('mbti'),
                army=request.session.get('army'),
                height=request.session.get('height'),
                body=request.session.get('body'),
                eyes=request.session.get('eyes'),
                face=request.session.get('face'),
                hobby=hobby_list  # 리스트로 저장
            )
            request.session.clear()
            return redirect("/success/")  # 모든 정보를 입력한 후 성공 페이지로 이동
        else:
            return redirect(f"/my/{index2}")  # 다음 페이지로 이동

    context = {'count': index}
    return render(request, "myapp/my.html", context)

'''
이런 방식을 사용해도 된다
def my(request):
    article = 'my'
    template = loader.get_template(myapp/my.html)
    context = {"article":article}
    return HttpResponse(template.render(context,request))

'''
@csrf_exempt
def you(request):
    article = 'you'
    context = {"article":article}
    return render(request, "myapp/you.html", context)

@csrf_exempt
def choose(request):
    #홍대축제에서 만나기 누르면 choose에서는 무조건 meeting으로 redirect
    return render(request, "myapp/choose.html")
      
@csrf_exempt
def matching(request):
    article = 'matching'
    context = {"article":article}
    return render(request, "myapp/matching.html", context)
    
@csrf_exempt
def matching2(request):

    return render(request, "myapp/matching2.html")
@csrf_exempt
def matching3(request):

    return render(request, "myapp/matching3.html")
@csrf_exempt
def error(request):

    return render(request, "myapp/error.html")
@csrf_exempt
def result(request):
    access_token = request.session.get("access_token",None)
    if access_token == None: #로그인 안돼있으면
        return render(request,"myapp/kakaologin.html") #로그인 시키기
    return render(request,"myapp/result.html")
    
@csrf_exempt
def menu(request):
    access_token = request.session.get("access_token",None)
    if access_token == None: #로그인 안돼있으면
        return render(request,"myapp/kakaologin.html") #로그인 시키기
    return render(request,"myapp/menu.html")


from django.shortcuts import render
from django.db.models import Q
from .models import Info
#from .service import UserProfileService



#소개팅에서 항목별로 값을 리스트로 받았을 때의 매칭 알고리즘
def match_profiles(category01, values01, category02, values02, user_gender):
    matches = Info.objects.all()

    # 상대방 성별과 맞지 않는 경우만 필터링
    if user_gender == 'M':
        matches = matches.filter(gender='F')
    elif user_gender == 'F':
        matches = matches.filter(gender='M')

    # 첫 번째 항목의 값과 일치하는 프로필 필터
    values01_filter = Q()
    for value in values01:
        if category01 == 'mbti':
            values01_filter |= Q(mbti=value)
        elif category01 == 'height':
            values01_filter |= Q(height=value)
        elif category01 == 'age':
            values01_filter |= Q(age=value)
        elif category01 == 'body':
            values01_filter |= Q(body=value)
        elif category01 == 'eyes':
            values01_filter |= Q(eyes=value)
        elif category01 == 'hobby':
            values01_filter |= Q(hobby=value)
        else:
            values01_filter |= Q(major=value)

    # 두 번째 항목의 값과 일치하는 프로필 필터
    values02_filter = Q()
    for value in values02:
        if category02 == 'mbti':
            values02_filter |= Q(mbti=value)
        elif category02 == 'height':
            values02_filter |= Q(height=value)
        elif category02 == 'age':
            values02_filter |= Q(age=value)
        elif category02 == 'body':
            values02_filter |= Q(body=value)
        elif category02 == 'eyes':
            values02_filter |= Q(eyes=value)
        elif category02 == 'hobby':
            values02_filter |= Q(hobby=value)
        else:
            values02_filter |= Q(major=value)

    # 두 가지 항목 모두 일치하는 프로필 검색
    both_values_matches = matches.filter(values01_filter & values02_filter)

    # 만약 두 가지 항목 모두 일치하는 프로필이 없을 경우
    if not both_values_matches.exists():
        # 하나라도 일치하는 프로필 검색
        either_value_matches = matches.filter(values01_filter | values02_filter)
        return either_value_matches
    else:
        return both_values_matches


#미팅에서 항목 별로 값을 리스트로 받았을 때의 매칭 알고리즘
def match_info_profiles(user_gender, peoplenum, ages, jobs):
    matches = Info.objects.all()

    # 상대방 성별과 맞지 않는 경우만 필터링
    if user_gender == 'male':
        matches = matches.filter(sex='female')
    elif user_gender == 'female':
        matches = matches.filter(sex='male')
    print("Matches after gender filtering:", matches)
    # peoplenum은 리스트 값 중 하나라도 일치하면 필터링
    peoplenum_filter = Q()

    # 현재 사용자의 peoplenum 값을 파싱하여 리스트로 변환
    user_peoplenum_list = [int(num) for num in peoplenum.split(',')]

    # Q 쿼리셋을 이용하여 하나라도 겹치면 프로필을 출력하도록 필터링
    for num in user_peoplenum_list:
        peoplenum_filter |= Q(peoplenum__contains=str(num))

    peoplenum_matches = matches.filter(peoplenum_filter)
    print("Matches after peoplenum filtering:", peoplenum_matches)
    # ages와 jobs 모두 일치하는 프로필 필터
    ages_filter = Q()
    for age_range in ages:
        start_age, end_age = map(int, age_range.split('-'))
        ages_filter |= Q(avgage__range=(start_age, end_age))
    both_values_matches = peoplenum_matches.filter(ages_filter, job__in=jobs)
    print("Matches after both values filtering:", both_values_matches)
    if both_values_matches.exists():
        return both_values_matches
    else:
        # 만약 모두 일치하는 프로필이 없을 경우, 하나라도 일치하는 프로필 필터
        either_values_matches = peoplenum_matches.filter(
            Q(ages_filter) | Q(job__in=jobs)
        )

        if either_values_matches.exists():
            return either_values_matches
        else:
            # 셋 중 하나만 일치하는 프로필 필터
            return peoplenum_matches.filter(
                Q(ages_filter) | Q(job__in=jobs)
            )


# 소개팅 매칭 함수
def perform_matching(request):
    if request.method == 'POST':
        # POST 요청으로 넘어온 데이터 받기
        category01 = request.POST.get('category01')
        values01 = request.POST.getlist('values01')
        category02 = request.POST.get('category02')
        values02 = request.POST.getlist('values02')
        user_gender = request.POST.get('user_gender')

        # 소개팅 알고리즘 돌린 후 조건에 맞는 프로필을 모두 matched_profiles 에 저장
        matched_profiles = match_profiles(category01, values01, category02, values02, user_gender)

        return render(request, 'myapp/youinfo.html', {'matched_profiles': matched_profiles})

    return render(request, 'myapp/youinfo.html')  # GET 요청에 대한 처리

# 미팅 매칭 함수
def perform_info_matching(request):
    access_token = request.session.get("access_token", None)
    if access_token == None:  # 로그인 안돼있으면
        return render(request, "myapp/kakaologin.html")  # 로그인 시키기

    account_info = requests.get("https://kapi.kakao.com/v2/user/me",
                                headers={"Authorization": f"Bearer {access_token}"}).json()
    if request.method == 'GET':
        kakao_id = account_info.get("id")
        print("kakao_id : ", kakao_id)

        # 예를 들어 사용자의 정보가 다음과 같다면:
        user_info = Info.objects.get(kakao_id=1)
        user_gender = user_info.sex
        peoplenum = user_info.peoplenum
        ages = user_info.ages.split(',')
        jobs = user_info.jobs.split(',')

        matched_profiles = match_info_profiles(user_gender, peoplenum, ages, jobs)
        #matched_profiles = Info.objects.get(kakao_id=1)
        return render(request, 'myapp/youinfo.html', {'matched_profiles': matched_profiles})

    return render(request, 'myapp/youinfo.html')  # GET 요청에 대한 처리

#카카오톡 아이디를 고유 값으로 받아 정보 분리해서 저장