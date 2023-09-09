from allauth.socialaccount.models import SocialAccount
import ast
from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Info
from myproject import settings
import requests
from django.template import loader
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.db.models import Q

# Create your views here.
  
@csrf_exempt
def index(request):
   return redirect("/home")

def kakaologin(request):
    #context = {'check':False} 지운다?
    access_token = request.session.get("access_token",None)
    if access_token: #만약 세션에 access_token이 있으면(==로그인 되어 있으면)
        account_info = requests.get("https://kapi.kakao.com/v2/user/me",
                                    headers={"Authorization": f"Bearer {access_token}"}).json()
        kakao_id = account_info.get("id")
        try:
            user_profile = Info.objects.get(kakao_id=kakao_id)  # 카카오톡 ID를 사용하여 사용자 정보 조회
            #print(kakao_id) 지운다?
            #context['user_profile'] = user_profile 지운다?
        except Info.DoesNotExist:
            # 새로운 레코드 생성
            user_profile = Info(kakao_id=kakao_id)
            user_profile.save()
            #context['user_profile'] = user_profile 지운다?

        return redirect("/home")  # 로그인 되어있으면 home페이지로 #로그인 되어있으면 home페이지로

    return render(request,"myapp/kakaologin.html")#로그인 안되어있으면 로그인페이지로

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
    request.session['access_token'] = _result['access_token']
    request.session.modified = True
    
    return redirect("/home") #로그인 완료 후엔 home페이지로

def kakaoLogout(request):
    access_token = request.session.get("access_token",None)
    if access_token == None: #로그인 안돼있으면
        return redirect("/kakaologin") #무지성 로그아웃 누른애는 로그인하도록 로그인창으로 보내기

    else:
        del request.session['access_token']
        return render(request, 'myapp/loginoutsuccess.html')


@csrf_exempt
def home(request):
    logged = 0
    
    access_token = request.session.get("access_token",None)
    if access_token:
        logged = 1
        account_info = requests.get("https://kapi.kakao.com/v2/user/me",
                                headers={"Authorization": f"Bearer {access_token}"}).json()
        kakao_id = account_info.get("id")
        user_info = Info.objects.filter(kakao_id=kakao_id).first()
        if user_info.kakaotalk_id :
            logged = 2
    context = {'logged':logged}
    return render(request, "myapp/home.html",context)

@csrf_exempt
def meeting(request):
    #만약 자기소개 정보가 없으면
    #return redirect('/my/1')
    access_token = request.session.get("access_token", None)
    if access_token:
        logged = 1
        account_info = requests.get("https://kapi.kakao.com/v2/user/me",
                                    headers={"Authorization": f"Bearer {access_token}"}).json()


    if request.method == "POST": # /home/meeting페이지로 인원 선택한 정보 전달
        peoplenum = ''
        peoplenum = request.POST.get('submit_peoplenum') #인원 선택 정보 추출
        avgage = request.POST.get('submit_age')

        kakao_id = account_info.get("id")
        user_info = Info.objects.filter(kakao_id=kakao_id).first()

        if user_info is None:
        # 사용자 정보가 없으면 새로 생성하고 저장
            user_info = Info.objects.create(
            kakao_id=kakao_id,
            peoplenum=', '.join(peoplenum),
            avgage=avgage
        )
        else:
        # 사용자 정보가 이미 있으면 업데이트
            user_info.peoplenum = ', '.join(peoplenum)
            user_info.avgage = avgage
            user_info.save()
        return redirect("/meeting2")  # /home/meeting2로 페이지 전달

    return render(request, "myapp/meeting.html")


@csrf_exempt
def meeting2(request):
    access_token = request.session.get("access_token", None)
    if access_token:
        logged = 1
        account_info = requests.get("https://kapi.kakao.com/v2/user/me",
                                    headers={"Authorization": f"Bearer {access_token}"}).json()


    if request.method == "POST":  # /home/meeting2 로 선호 직업, 장소, 나이 전달
        jobs = request.POST.get('submit_job').split(', ')
        ages = request.POST.get('submit_age').split(', ')  # ', '로 파싱해서 데이터베이스 저장

        kakao_id = account_info.get("id")

        user_info = Info.objects.filter(kakao_id=kakao_id).first()

        if user_info is None:
            # 사용자 정보가 없으면 새로 생성하고 저장
            user_info = Info.objects.create(
                kakao_id=kakao_id,
                jobs=', '.join(jobs),
                ages=', '.join(ages),
                matching_application=1  # 매칭 신청 여부를 True로 설정
            )
        else:
            # 사용자 정보가 이미 있으면 업데이트
            user_info.jobs = ', '.join(jobs)
            user_info.ages = ', '.join(ages)
            user_info.matching_application = True  # 매칭 신청 여부를 True로 설정
            user_info.save()

        return redirect("/good/")

    return render(request, "myapp/meeting2.html")

@csrf_exempt
def good(request):

    return render(request, "myapp/good.html")

@csrf_exempt
def go(request):

    return render(request, "myapp/go.html")


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

def kakao(request):
    access_token = request.session.get("access_token", None)
    if access_token == None:  # 로그인 안돼있으면
        return render(request, "myapp/kakaologin.html")  # 로그인 시키기

    account_info = requests.get("https://kapi.kakao.com/v2/user/me",
                                headers={"Authorization": f"Bearer {access_token}"}).json()
    if request.method == 'GET':
        kakao_id = account_info.get("id")

        user_info = Info.objects.get(kakao_id=kakao_id)
        user_gender = user_info.sex
        peoplenum = user_info.peoplenum
        ages = user_info.ages.split(',')
        jobs = user_info.jobs.split(',')

        matched_profiles = match_info_profiles(user_gender, peoplenum, ages, jobs)

        if matched_profiles:
            first_matched_profile = matched_profiles[0]
            return render(request, 'myapp/kakao.html', {'matched_profiles': first_matched_profile})

    return render(request, "myapp/kakao.html")

@csrf_exempt
def major(request):

    return render(request, "myapp/major.html")
@csrf_exempt
def mbti(request):

    return render(request, "myapp/mbti.html")

@csrf_exempt
def myinfo(request):
    access_token = request.session.get("access_token",None)
    if access_token == None: #로그인 안돼있으면
        return render(request,"myapp/kakaologin.html") #로그인 시키기

    account_info = requests.get("https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"}).json()
    kakao_id = account_info.get("id")
    
    user_profile = get_object_or_404(Info, kakao_id=kakao_id)
    context = {'user_profile': user_profile,  # 사용자 정보를 context에 추가
    }
    return render(request, "myapp/myinfo.html",context)
@csrf_exempt
def success(request):
    access_token = request.session.get("access_token", None)
    if access_token == None:  # 로그인 안돼있으면
        return render(request, "myapp/kakaologin.html")  # 로그인 시키기

    account_info = requests.get("https://kapi.kakao.com/v2/user/me",
                                headers={"Authorization": f"Bearer {access_token}"}).json()

    kakao_id = account_info.get("id")

    if request.method == 'GET':
        kakao_id = account_info.get("id")
        print("kakao_id: ", kakao_id)

        user_info = Info.objects.get(kakao_id=kakao_id)
        user_gender = user_info.sex
        peoplenum = user_info.peoplenum
        ages = user_info.ages.split(',')
        jobs = user_info.jobs.split(',')

        matched_profiles = match_info_profiles(user_gender, peoplenum, ages, jobs)
        first_matched_profile = matched_profiles[0]

        user_info.matching_agreement = True
        user_info.save()

        if user_info.matching_agreement == True and first_matched_profile.matching_agreement == True:
            user_info.matching_success = 1
            user_info.save()
            first_matched_profile.matching_success = 1
            first_matched_profile.save()

    return render(request, 'myapp/matching.html')




    return render(request, "myapp/success.html")

@csrf_exempt
def fail(request):

    return render(request, "myapp/fail.html")

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
    if access_token:
        logged = 1
        account_info = requests.get("https://kapi.kakao.com/v2/user/me",
                                    headers={"Authorization": f"Bearer {access_token}"}).json()


    kakao_id = account_info.get("id")

    if request.method == "GET":
        if int(id) == 1:
            if request.session.get('current_page'):
                del request.session['current_page']

        current_page = request.session.get('current_page', 0)
        if int(id) < current_page:
            current_page = int(id)

        if not is_valid_transition(current_page, id):
            # 올바른 페이지 이동이 아니면 거부
            if current_page == 2 and int(id) == 4 and request.session['sex'] == 'female':  # 여자면 4로 이동되도록 함. 3이 army여야함
                request.session['current_page'] = int(id) - 1
                return redirect("/my/4")
            return HttpResponseForbidden("Forbidden")

        # 페이지 이동을 허용하고, 세션 업데이트
        request.session['current_page'] = int(id)

    # 자기소개 한거 있으면 자기소개 내용 불러오고 choose페이지로 넘어가게

    index = int(id)

    if request.method == "POST":
        if index == 1:
            request.session['age'] = request.POST.get("age")
        elif index == 2:
            request.session['sex'] = request.POST.get("sex")
            if request.session['sex'] == 'female':
                # request.session['army'] = 'female' 이런식으로 여자면 army값을 넣어줘야함 안그러면 아래에서 NULL입력돼서 매칭 안됨
                index += 1
        elif index == 3:
            request.session['army'] = request.POST.get("army")
        elif index == 4:
            request.session['job'] = request.POST.get("job")
        elif index == 5:
            request.session['school'] = request.POST.get("school")
            request.session['major'] = request.POST.get("major")
        elif index == 6:
            selected_mbti = []
            for i in range(1, 5):
                mbti_value = request.POST.get(f"mbti{i}")
                if mbti_value:
                    selected_mbti.append(mbti_value)
            selected_mbti_str = ''.join(selected_mbti)
            request.session['mbti'] = selected_mbti_str
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
            hobby_str = ', '.join(hobby_list)  # 선택한 취미를 문자열로 합치기
            request.session['hobby'] = hobby_str  # 세션에 저장
        elif index == 12:
            request.session['free'] = request.POST.get("free")
        else:
            index = 1

        index2 = index + 1
        if index2 > 12:  # 모든 정보를 입력한 경우
            # 세션에 저장된 정보를 하나의 Info 객체에 저장하고 세션 초기화
            user_info = Info.objects.filter(kakao_id=kakao_id).first()
            if user_info:
                user_info.age = request.session.get('age')
                user_info.sex = request.session.get('sex')
                user_info.job = request.session.get('job')
                user_info.school = request.session.get('school')
                user_info.major = request.session.get('major')
                user_info.mbti = request.session.get('mbti')
                user_info.army = request.session.get('army')
                user_info.height = request.session.get('height')
                user_info.body = request.session.get('body')
                user_info.eyes = request.session.get('eyes')
                user_info.face = request.session.get('face')
                user_info.hobby = request.session.get('hobby')
                user_info.free = request.session.get('free')
                user_info.save()
            else:
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
                    eyes=request.session.get('body'),
                    face=request.session.get('face'),
                    hobby=request.session.get('hobby'),
                    free=request.session.get('free')
                )
            return redirect("/kakaoid/")  # 모든 정보를 입력한 후 성공 페이지로 이동
        else:
            return redirect(f"/my/{index2}")  # 다음 페이지로 이동

    context = {'count': index}
    return render(request, "myapp/my.html", context)
    

@csrf_exempt
def you(request):

    return render(request, "myapp/you.html")

@csrf_exempt
def choose(request):
    #홍대축제에서 만나기 누르면 choose에서는 무조건 meeting으로 redirect
    return render(request, "myapp/choose.html")
      
@csrf_exempt
def matching(request):
    access_token = request.session.get("access_token", None)
    if access_token is None:
        return render(request, "myapp/kakaologin.html")

    account_info = requests.get("https://kapi.kakao.com/v2/user/me",
                                headers={"Authorization": f"Bearer {access_token}"}).json()

    if request.method == 'GET':
        kakao_id = account_info.get("id")
        print("kakao_id: ", kakao_id)

        user_info = Info.objects.get(kakao_id=kakao_id)
        user_gender = user_info.sex
        peoplenum = user_info.peoplenum
        ages = user_info.ages.split(',')
        jobs = user_info.jobs.split(',')

        matched_profiles = match_info_profiles(user_gender, peoplenum, ages, jobs)
        first_matched_profile = matched_profiles[0]

        if first_matched_profile:
            user_info.matching_success = 1
            user_info.you_kakao_id = first_matched_profile.kakao_id
            user_info.matching_time = timezone.now()
            user_info.save()  # 사용자의 matching_success 필드를 True로 저장

            # 상대방의 matching_success 필드도 업데이트

            if first_matched_profile.matching_success != 1:
                first_matched_profile.matching_success = 1
                first_matched_profile.you_kakao_id = kakao_id
                first_matched_profile.matching_time = timezone.now()
                first_matched_profile.save()

            else:
                user_info.matching_success = 0
                user_info.you_kakao_id = ''
                user_info.save()

            # 매칭 성사 후 한 시간이 지났는지 확인


            return render(request, 'myapp/matching.html', {'matched_profile': first_matched_profile})
        else:

            user_info.matching_success = 2
            no_match_message = "매칭된 상대가 없습니다."
            return render(request, 'myapp/matching.html', {'no_match_message': no_match_message})

    return render(request, 'myapp/matching.html')
    
@csrf_exempt
def matching2(request):
    access_token = request.session.get("access_token", None)
    if access_token is None:
        return render(request, "myapp/kakaologin.html")

    account_info = requests.get("https://kapi.kakao.com/v2/user/me",
                                headers={"Authorization": f"Bearer {access_token}"}).json()

    if request.method == 'GET':
        kakao_id = account_info.get("id")
        print("kakao_id: ", kakao_id)

        user_info = Info.objects.get(kakao_id=kakao_id)
        user_gender = user_info.sex
        peoplenum = user_info.peoplenum
        ages = user_info.ages.split(',')
        jobs = user_info.jobs.split(',')

        matched_profiles = match_info_profiles(user_gender, peoplenum, ages, jobs)
        first_matched_profile = matched_profiles[0]

        if first_matched_profile:
            user_info.matching_success = 1
            user_info.you_kakao_id = first_matched_profile.kakao_id
            user_info.matching_time = timezone.now()
            user_info.save()  # 사용자의 matching_success 필드를 True로 저장

            # 상대방의 matching_success 필드도 업데이트

            if first_matched_profile != 1:
                first_matched_profile.matching_success = 1
                first_matched_profile.you_kakao_id = kakao_id
                first_matched_profile.matching_time = timezone.now()
                first_matched_profile.save()

            else:
                user_info.matching_success = 0
                user_info.you_kakao_id = ''
                user_info.save()

            # 매칭 성사 후 한 시간이 지났는지 확인


            return render(request, 'myapp/matching2.html', {'matched_profile': first_matched_profile})
        else:

            user_info.matching_success = 2
            no_match_message = "매칭된 상대가 없습니다."
            return render(request, 'myapp/matching2.html', {'no_match_message': no_match_message})

    return render(request, 'myapp/matching2.html')
@csrf_exempt
def matching3(request):

    return render(request, "myapp/matching3.html")
@csrf_exempt
def error(request):

    return render(request, "myapp/error.html")

@csrf_exempt
def use(request):

    return render(request, "myapp/use.html")

def result(request):  # 추후 보강 해야함(09.07)
    access_token = request.session.get("access_token", None)
    if access_token == None:  # 로그인 안돼있으면
        return render(request, "myapp/kakaologin.html")  # 로그인 시키기

    account_info = requests.get("https://kapi.kakao.com/v2/user/me",
                                headers={"Authorization": f"Bearer {access_token}"}).json()
    if request.method == 'GET':
        kakao_id = account_info.get("id")

        # 예를 들어 사용자의 정보가 다음과 같다면:
        user_info = Info.objects.get(kakao_id=kakao_id)
    return render(request, "myapp/result.html", {'user_info': user_info})
@csrf_exempt
def menu(request):

    return render(request,"myapp/menu.html")

@csrf_exempt
def kakaoid(request):
    access_token = request.session.get("access_token",None)
    if access_token == None: #로그인 안돼있으면
        return redirect("/kakaologin")

    account_info = requests.get("https://kapi.kakao.com/v2/user/me",headers={"Authorization": f"Bearer {access_token}"}).json()

    if request.method == "POST":
        kakao_id = account_info.get("id")

        # kakao_id를 사용하여 해당 사용자의 레코드 가져오기
        user_info = Info.objects.filter(kakao_id=kakao_id).first()

        kakaotalk_id = request.POST.get("kakaoid")
        if kakaotalk_id is not None:
            # 가져온 레코드에 kakaotalk_id 할당 및 저장
            user_info.kakaotalk_id = kakaotalk_id
            user_info.save()
            return redirect("/go")
        else:
            return HttpResponse("ID를 입력해주세요")

    return render(request, "myapp/kakaoid.html")

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

def perform_info_matching(request):
    access_token = request.session.get("access_token", None)
    if access_token is None:
        return render(request, "myapp/kakaologin.html")

    account_info = requests.get("https://kapi.kakao.com/v2/user/me",
                                headers={"Authorization": f"Bearer {access_token}"}).json()

    if request.method == 'GET':
        kakao_id = account_info.get("id")
        print("kakao_id: ", kakao_id)

        user_info = Info.objects.get(kakao_id=kakao_id)
        user_gender = user_info.sex
        peoplenum = user_info.peoplenum
        ages = user_info.ages.split(',')
        jobs = user_info.jobs.split(',')

        matched_profiles = match_info_profiles(user_gender, peoplenum, ages, jobs)

        if matched_profiles:
            first_matched_profile = matched_profiles[0]
            return render(request, 'myapp/youinfo.html', {'matched_profile': first_matched_profile})
        else:
            no_match_message = "매칭된 상대가 없습니다."
            return render(request, 'myapp/youinfo.html', {'no_match_message': no_match_message})

    return render(request, 'myapp/youinfo.html')