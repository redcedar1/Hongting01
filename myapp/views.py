from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Info
from myproject import settings
import requests
from django.template import loader
from django.http import HttpResponse, JsonResponse

# Create your views here.
  
count = 0
@csrf_exempt
def index(request):
   return render(request, 'myapp/index.html')



def kakaologin(request):
    context = {'check': False}
    if request.session.get('access_token'):
        access_token = request.session.get('access_token')
        account_info = requests.get("https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"}).json()
        kakao_id = account_info.get("id")

        try:
            user_profile = Info.objects.get(kakao_id=kakao_id)  # 카카오톡 ID를 사용하여 사용자 정보 조회
            context['user_profile'] = user_profile
        except Info.DoesNotExist:
            # 새로운 레코드 생성
            user_profile = Info(kakao_id=kakao_id)
            user_profile.save()
            context['user_profile'] = user_profile

        return render(request, "myapp/kakaologin.html", context)

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
    
    return render(request, 'myapp/meeting2.html')

def kakaoLogout(request):
    
    _token = request.session['access_token']
    _url = 'https://kapi.kakao.com/v1/user/logout'
    _header = {
      'Authorization': f'bearer {_token}'
    }
    # _url = 'https://kapi.kakao.com/v1/user/unlink'
    # _header = {
    #   'Authorization': f'bearer {_token}',
    # }
    _res = requests.post(_url, headers=_header)
    _result = _res.json()
    
    print(_result.get('id'))#액세스 토큰은 바뀌어도 id값은 안바뀌니 이것으로 조회 가능
    if _result.get('id'):
        
        del request.session['access_token']
        return render(request, 'myapp/loginoutsuccess.html')
    else:
        return render(request, 'myapp/logouterror.html')


@csrf_exempt
def home(request):
    article = 'home is here'
    context = {"article":article}
    return render(request, "myapp/home.html", context)

@csrf_exempt
def meeting(request):
    global count
    if request.method == "POST": # /home/meeting페이지로 인원 선택한 정보 전달
        peoplenum = ''
        peoplenum = request.POST.get('submit_peoplenum') #인원 선택 정보 추출
        if peoplenum == '': #인원 값이 없으면
            errormsg = {"error_message": "인원을 선택하지 않으셨습니다."}
            return render(request, "myapp/meeting.html", errormsg)
        q = Info.objects.create(peoplenums=peoplenum)
        q.save()
        count = q.id
        print(count)
        return redirect("/meeting2")# /home/meeting2로 페이지 전달
    return render(request, "myapp/meeting.html")


@csrf_exempt
def meeting2(request):
    global count
    if request.method == "POST": # /home/meeting2 로 선호 직업, 장소, 나이 전달
        job = request.POST.get('submit_job')
        location = request.POST.get('submit_location')
        age = request.POST.get('submit_age')
        print(job)
        print(location)
        print(age)

        if job == '' or location =='': #인원 값이 없으면
            errormsg = {"error_message": "모든 필드에서 최소 한가지를 선택해 주세요."}
            return render(request, "myapp/meeting2.html", errormsg)

        q = Info.objects.latest('kakao_id')#마지막으로 생성된 아이디에 저장??
        q.jobs = job
        q.locations = location
        q.ages = age
        q.save()
        return redirect("/home/")

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

    return render(request, "myapp/kakao.html")
@csrf_exempt
def major(request):

    return render(request, "myapp/major.html")
@csrf_exempt
def mbti(request):

    return render(request, "myapp/mbti.html")

myinfo = {}
@csrf_exempt
def myinfo(request, id):
    access_token = request.session.get("access_token")
    account_info = requests.get("https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"}).json()
    email = account_info.get("kakao_account", {}).get("email")
    nickname = account_info.get("kakao_account", {}).get("nickname")


    user_profile = Info.objects.get(pk=id)  # 사용자의 id 값 얻어옴

    # id 값을 사용하여 사용자 정보 조회
    try:
        user_profile = Info.objects.get(id=id)
    except Info.DoesNotExist:
        user_profile = None  # 해당 id로 사용자 정보를 찾을 수 없는 경우

    context = {'email': email, 'nickname': nickname, 'user_profile': user_profile}

    return render(request, "myapp/myinfo.html", context)
@csrf_exempt
def success(request):

    return render(request, "myapp/success.html")
@csrf_exempt
def youinfo(request):

    return render(request, "myapp/youinfo.html")

@csrf_exempt
def my(request, id):
    index = int(id)

    if request.method == "POST":
        if index == 1:
            request.session['age'] = request.POST.get("age")
        elif index == 2:
            request.session['sex'] = request.POST.get("sex")
        elif index == 3:
            request.session['peoplenum'] = request.POST.get("peoplenum")
        elif index == 4:
            request.session['job'] = request.POST.get("job")
        elif index == 5:
            request.session['school'] = request.POST.get("school")
            request.session['major'] = request.POST.get("major")
        elif index == 6:
            request.session['mbti'] = request.POST.get("mbti")
        elif index == 7:
            request.session['army'] = request.POST.get("army")
        elif index == 8:
            request.session['height'] = request.POST.get("height")
        elif index == 9:
            request.session['body'] = request.POST.get("body")
        elif index == 10:
            request.session['eyes'] = request.POST.get("eyes")
        elif index == 11:
            request.session['face'] = request.POST.get("face")
        elif index == 12:
            request.session['hobby'] = request.POST.get("hobby")

        index2 = index + 1
        if index2 > 12:  # 모든 정보를 입력한 경우
            # 세션에 저장된 정보를 하나의 Info 객체에 저장하고 세션 초기화
            myinfo = Info.objects.create(
                age=request.session.get('age'),
                sex=request.session.get('sex'),
                peoplenum=request.session.get('peoplenum'),
                job=request.session.get('job'),
                school=request.session.get('school'),
                major=request.session.get('major'),
                mbti=request.session.get('mbti'),
                army=request.session.get('army'),
                height=request.session.get('height'),
                body=request.session.get('body'),
                eyes=request.session.get('eyes'),
                face=request.session.get('face'),
                hobby=request.session.get('hobby')

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
    article = 'result'
    context = {"article":article}
    return render(request, "myapp/result.html", context)
    
@csrf_exempt
def menu(request):
    article = 'menu'
    context = {"article":article}
    return render(request, "myapp/menu.html", context)
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
def match_info_profiles(locations, ages, user_gender, peoplenum):
    gender_filter = ~Q(gender=user_gender)
    peoplenum_filter = Q()
    for num in peoplenum:
        peoplenum_filter |= Q(peoplenum=num)

    # 두 가지 조건을 각각 필터링
    locations_filter = Q()
    for location in locations:
        locations_filter |= Q(meetinglocation=location)

    ages_filter = Q()
    for age in ages:
        ages_filter |= Q(ages=age)

    # 두 가지 조건을 모두 만족하는 프로필 필터
    two_conditions_filter = locations_filter & ages_filter

    # 두 가지 조건을 모두 만족하는 프로필 검색
    two_matches = Info.objects.filter(gender_filter & peoplenum_filter & two_conditions_filter)

    # 두 가지 조건을 모두 만족하는 프로필이 없을 경우
    if not two_matches.exists():
        # 한 가지 조건을 만족하는 프로필 필터
        one_matches = Info.objects.filter(gender_filter & peoplenum_filter & (locations_filter | ages_filter))
        return one_matches
    else:
        return two_matches


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

        return render(request, 'youinfo.html', {'matched_profiles': matched_profiles})

    return render(request, 'youinfo.html')  # GET 요청에 대한 처리

# 미팅 매칭 함수
def perform_info_matching(request, id):
    if request.method == 'POST':
        # 사용자의 id 값을 사용하여 데이터베이스에서 사용자 정보를 가져옴
        user_profile = Info.objects.get(pk=id)

        # 사용자 정보에서 locations와 ages 값을 얻어옴
        locations = user_profile.locations
        ages = user_profile.ages
        user_gender = user_profile.gender
        peoplenum = user_profile.peoplenum


        # 소개팅 알고리즘 돌린 후 조건에 맞는 프로필을 모두 matched_profiles 에 저장
        matched_profiles = match_info_profiles('locations', locations, 'ages', ages, user_gender, peoplenum)

        return render(request, 'youinfo.html', {'matched_profiles': matched_profiles})

    return render(request, 'youinfo.html')  # GET 요청에 대한 처리

#카카오톡 아이디를 고유 값으로 받아 정보 분리해서 저장