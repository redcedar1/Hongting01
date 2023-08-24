var count=1;

function count() {
    count++;
    if(count==14) location.href = '/choose/';
}

function createStr() {
    if(count==1) document.write("나이를 입력해주세요!");
    else if(count==2) document.write("성별");
    else if(count==3) document.write("원하는 미팅 인원수");
    else if(count==4) document.write("직업"); //대학생, 대학원생, 취준생, 직장인
    else if(count==5) document.write("학교와 학과"); //학교 인증 시스템 넣기
    else if(count==6) document.write("mbti");
    else if(count==7) document.write("군/미필");
    else if(count==8) document.write("키"); //범위로(5단위)
    else if(count==9) document.write("체형"); //탭으로(마름, 보통, 통통, 근육)
    else if(count==10) document.write("유/무쌍"); //탭으로
    else if(count==11) document.write("얼굴상"); //뚜렷, 두부
    else if(count==12) document.write("관심사"); //탭으로
    else if(count==13) {
        document.write("자유로운 자기소개<br>");
        document.write("최소 10자의 자기소개를 적어주세요.<br>");
        document.write("자기소개를 길게 쓸수록 <br> 매칭확률이 높아집니다.");
    }
}

function create() {
    const elem= document.getElementById("form");
    if(count==1) {
        elem.innerHTML = "<input type=text name=age id=input1 size=10 required></input>";
    }
    else if(count==2) {
        elem.innerHTML = "<input type=radio name=sex id=male required> <label for=male> 남성 </label>\
                <input type=radio name=sex id=female required> <label for=female> 여성 </label>"
    }
    else if(count==3) {
        elem.innerHTML = "<input type=checkbox name=peoplenum id=one value=1 > <label for = one> 소개팅 </label> \
                <input type=checkbox name=peoplenum id=two value=2 required> <label for = two> 2명이서 </label>\
                <input type=checkbox name=peoplenum id=three value=3 > <label for = three> 3명이서 </label> \
                <input type=checkbox name=peoplenum id=four value=4 > <label for = four> 4명이서 </label> "
    }
    else if(count==4) {
        elem.innerHTML = "<input type=radio name=job id=1  > <label for = 1> 대학생 </label> \
                 <input type=radio name=job id=2 value=대학원생> <label for = 2> 대학원생 </label> \
                 <input type=radio name=job id=3 value=취준생 > <label for = 3> 취준생 </label> \
                 <input type=radio name=job id=4 value=직장인 > <label for = 4> 직장인 </label> "
    }
    else if(count==5) {
        elem.innerHTML = "<input type=text name=school placeholder=학교 size=10 required></input>\
        <br><br>\
        <input type=radio id=1 name=major value=문과대 > <label for = 1> 문과대 </label>\
        <input type=radio id=2 name=major value=이과대> <label for = 2> 이과대 </label>\
        <input type=radio id=3 name=major value=사범대 > <label for = 3> 사범대 </label>\
        <input type=radio id=4 name=major value=체대> <label for = 4> 체대 </label>\
        <input type=radio id=5 name=major value=미대> <label for = 5> 미대 </label>\
        <input type=radio id=6 name=major value=예대> <label for = 6> 예대 </label>\
        <input type=radio id=7 name=major value=음대> <label for = 7> 음대 </label>\
        <input type=radio id=8 name=major value=의약대> <label for = 8> 의/약대 </label>\
        <input type=radio id=9 name=major value=특수대> <label for = 9> 특수대 </label> "
    }
    else if(count==6) {
        elem.innerHTML = "<input type=text name=mbti placeholder=mbti size=10 required></input>"
    }
    else if(count==7) {
        elem.innerHTML = "<input type=radio id=1 name=army value=군필 > <label for=1> 군필 </label> \
                <input type=radio id=2 name=army value=미필 required> <label for=2> 미필 </label>"
    }
    else if(count==8) {
        elem.innerHTML = "<input type=text id=height size=10 required></input>"
        
    }
    else if(count==9) {
        elem.innerHTML = "<input type=radio id=1 name=body value=마름 > <label for = 1> 마름 </label> \
                <input type=radio id=2 name=body value=보통> <label for = 2>  보통 </label>\
                <input type=radio id=3 name=body value=통통 > <label for = 3>  통통 </label> \
                <input type=radio id=4 name=body value=탄탄> <label for = 4>  탄탄 </label>"
    }
    else if(count==10) {
        elem.innerHTML = "<input type=radio id=1 name=eyes value=유쌍 > <label for = 1> 유쌍 </label> \
        <input type=radio id=2 name=eyes value=무쌍> <label for = 2>  무쌍 </label>"
    }
    else if(count==11) {
        elem.innerHTML = "<input type=radio id=1 name=face value=두부 > <label for = 1> 두부상 </label> \
        <input type=radio id=2 name=face value=뚜렷> <label for = 2> 뚜렷상 </label>"
    }
   
    else if(count==12) {
        elem.innerHTML = "<input type=checkbox name=hobby id=1 value=1 > <label for = 1> 운동 </label> \
                <input type=checkbox name=hobby id=2 value=2 required> <label for = 2> 산책 </label>\
                <input type=checkbox name=hobby id=3 value=3 > <label for = 3> 공연관람 </label> \
                <input type=checkbox name=hobby id=4 value=4 > <label for = 4> 쇼핑 </label> \
                <input type=checkbox name=hobby id=5 value=1 > <label for = 5> 재태크 </label> \
                <input type=checkbox name=hobby id=6 value=2 required> <label for = 6> 패션 </label>\
                <input type=checkbox name=hobby id=7 value=3 > <label for = 7> 반려동물 </label> \
                <input type=checkbox name=hobby id=8 value=4 > <label for = 8> 음악감상 </label>\
                <input type=checkbox name=hobby id=9 value=1 > <label for = 9> 독서 </label> \
                <input type=checkbox name=hobby id=10 value=2 required> <label for = 10> 여행 </label>\
                <input type=checkbox name=hobby id=11 value=3 > <label for = 11> 카페 </label> \
                <input type=checkbox name=hobby id=12 value=4 > <label for = 12> 게임 </label>\
                <input type=checkbox name=hobby id=13 value=2 required> <label for = 13> 영화/드라마 </label>\
                <input type=checkbox name=hobby id=14 value=3 > <label for = 14> 전시관람 </label> \
                <input type=checkbox name=hobby id=15 value=4 > <label for = 15> 연극/뮤지컬 </label>\
                <input type=checkbox name=hobby id=16 value=1 > <label for = 16> 술 </label> \
                <input type=checkbox name=hobby id=17 value=2 required> <label for = 17> 악기연주 </label>\
                <input type=checkbox name=hobby id=18 value=3 > <label for = 18> 맛집 </label> \
                <input type=checkbox name=hobby id=19 value=4 > <label for = 19> 요리 </label>"
    }
    else if(count==13) {
        elem.innerHTML = "<br> <textarea name=free id=input2 cols=40 rows=10> </textarea> \
        <p> 제출하면 자기소개가 완료됩니다! </p>"
    }
}

function major() {
    const elem= document.getElementById("form0");
    elem.innerHTML = "<input type=text id=input placeholder=학과 size=10 required></input> "
}