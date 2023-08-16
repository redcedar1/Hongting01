function createStr() {
    if(/*나이값 없으면*/ false) document.write("나이를 입력해주세요!");
    else if(/*성별값 없으면*/ false) document.write("성별");
    else if(/*미팅 인원수*/ false) document.write("원하는 미팅 인원수");
    else if(/*직업*/ false) document.write("직업"); //대학생, 대학원생, 취준생, 직장인
    else if(/*대학생이면*/ false) document.write("학교와 학과"); //학교 인증 시스템 넣기
    else if(/*mbti*/ false) document.write("mbti");
    else if(/*남자면*/ false) document.write("군/미필");
    else if(/*키*/ false) document.write("키"); //범위로(5단위)
    else if(/*체형*/ false) document.write("체형"); //탭으로(마름, 보통, 통통, 근육)
    else if(/*유/무쌍*/ false) document.write("유/무쌍"); //탭으로
    else if(/*얼굴상*/ false) document.write("얼굴상"); //뚜렷, 두부
    else if(/*관심사*/ true) document.write("관심사"); //탭으로
    else if(/*자유로운 자기소개*/ true) {
        document.write("자유로운 자기소개<br>");
        document.write("최소 10자의 자기소개를 적어주세요.<br>");
        document.write("자기소개를 길게 쓸수록 매칭확률이 높아집니다.");
    }
}
function create() {
    const elem= document.getElementById("form");
    if(/*나이값 없으면*/ false) {
        elem.innerHTML = "<input type=text id=input placeholder=나이 입력 size=10 required></input>"
    }
    else if(/*성별값 없으면*/ false) {
        elem.innerHTML = "<label> <input type=radio name=sex id=male required> \
                <label for=male> 남성 </label> \
                <label> <input type=radio name=sex id=female required> \
                <label for=female> 여성 </label>"
    }
    else if(/*미팅 인원수*/ false) {
        elem.innerHTML = "<label> <input type=checkbox value=1 > 소개팅 </label> \
                <label> <input type=checkbox value=2 required> 2명이서 </label>\
                <label> <input type=checkbox value=3 > 3명이서 </label> \
                <label> <input type=checkbox value=4 > 4명이서 </label> "
    }
    else if(/*직업*/ false) {
        elem.innerHTML = "<label> <input type=checkbox value=대학생 > 대학생 </label> \
                <label> <input type=checkbox value=대학원생> 대학원생 </label> \
                <label> <input type=checkbox value=취준생 > 취준생 </label> \
                <label> <input type=checkbox value=직장인 > 직장인 </label> "
    }
    else if(/*대학생이면*/ true) {
        elem.innerHTML = "<input type=text id=input placeholder=학교 size=10 required></input>\
        <label> <input type=checkbox value=문과대 > 문과대 </label>\
        <label> <input type=checkbox value=이과대> 이과대 </label>\
        <label> <input type=checkbox value=사범대 > 사범대 </label>\
        <label> <input type=checkbox value=체대> 체대 </label>\
        <label> <input type=checkbox value=미대> 미대 </label>\
        <label> <input type=checkbox value=예대> 예대 </label>\
        <label> <input type=checkbox value=음대> 음대 </label>\
        <label> <input type=checkbox value=의약대> 의/약대 </label>\
        <label> <input type=checkbox value=특수대> 특수대 </label> "
    }
    else if(/*mbti*/ false) {
        elem.innerHTML = "<input type=text id=input placeholder=mbti size=10 required></input>"
    }
    else if(/*남자면*/ false) {
        elem.innerHTML = "<label> <input type=checkbox value=군필 > 군필 </label> \
                <label> <input type=checkbox value=미필 required> 미필 </label>"
    }
    else if(/*키*/ false) {
        elem.innerHTML = "<label> <input type=checkbox value=150미만 > 150미만 </label> \
                <label> <input type=checkbox value=155> 150~155 </label>\
                <label> <input type=checkbox value=160 > 155~160 </label> \
                <label> <input type=checkbox value=165> 160~165 </label>\
                <label> <input type=checkbox value=170 > 165~170 </label> \
                <label> <input type=checkbox value=175> 170~175 </label>\
                <label> <input type=checkbox value=180 > 175~180 </label> \
                <label> <input type=checkbox value=185 > 180~185 </label>\
                <label> <input type=checkbox value=190 > 185~190 </label> \
                <label> <input type=checkbox value=190이상 > 190이상</label> "
    }
    else if(/*체형*/ false) {
        elem.innerHTML = "<label> <input type=checkbox value=마름 > 마름 </label> \
                <label> <input type=checkbox value=보통> 보통 </label>\
                <label> <input type=checkbox value=통통 > 통통 </label> \
                <label> <input type=checkbox value=탄탄> 탄탄 </label>"
    }
    else if(/*유무쌍*/ false) {
        elem.innerHTML = "<label> <input type=checkbox value=유쌍 > 유쌍 </label> \
                <label> <input type=checkbox value=무쌍> 무쌍 </label>"
    }
    else if(/*얼굴상*/ false) {
        elem.innerHTML = "<label> <input type=checkbox value=뚜렷 > 뚜렷 </label> \
                <label> <input type=checkbox value=두부> 두부 </label>"
    }
    else if(/*관심사*/ true) {
        elem.innerHTML = "<label> <input type=checkbox> 운동 </label>\
        <label> <input type=checkbox> 산책 </label>\
        <label> <input type=checkbox> 공연관람 </label>\
        <label> <input type=checkbox> 쇼핑 </label>\
        <label> <input type=checkbox> 재태크 </label>\
        <label> <input type=checkbox> 패션 </label>\
        <label> <input type=checkbox> 반려동물 </label>\
        <label> <input type=checkbox> 음악감상 </label>\
        <label> <input type=checkbox> 독서 </label>\
        <label> <input type=checkbox> 여행 </label>\
        <label> <input type=checkbox> 카페 </label>\
        <label> <input type=checkbox> 게임 </label>\
        <label> <input type=checkbox> 영화/드라마 </label>\
        <label> <input type=checkbox> 전시관람 </label>\
        <label> <input type=checkbox> 연극/뮤지컬 </label>\
        <label> <input type=checkbox> 술 </label>\
        <label> <input type=checkbox> 악기연주 </label>\
        <label> <input type=checkbox> 맛집 </label>\
        <label> <input type=checkbox> 요리 </label> "
    }
    else if(/*자유로운 자기소개*/ true) {
        elem.innerHTML = "<br> <textarea id=input2 cols=40 rows=10> </textarea>"
    }
}

function ageLevel() {
    const elem= document.getElementById("form1");
    elem.innerHTML = "<p>매칭하길 원하는 나이대를 선택해주세요(다수선택 가능)</p> \
    <label> <input type=checkbox> 20살 \
    <input type=checkbox> 21살 \
    <input type=checkbox> 22살 \
    <input type=checkbox> 23살 \
    <input type=checkbox> 24살 \
    <input type=checkbox> 25살 \
    <input type=checkbox> 26살 \
    <input type=checkbox> 27살 \
    <input type=checkbox> 28살 \
    <input type=checkbox> 29살 \
     </label> "
}

function job() {
    const elem= document.getElementById("form2");
    elem.innerHTML = " <p>원하는 상대방의 직업을 선택해주세요(다수선택 가능)</p>\
    <label> <input type=checkbox value=대학생 > 대학생 </label> \
                <label> <input type=checkbox value=대학원생> 대학원생 </label> \
                <label> <input type=checkbox value=취준생 > 취준생 </label> \
                <label> <input type=checkbox value=직장인 > 직장인 </label> "
}

function major() {
    const elem= document.getElementById("form0");
    elem.innerHTML = "<input type=text id=input placeholder=학과 size=10 required></input> "
}