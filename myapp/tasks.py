from django.contrib.auth import get_user_model
from celery import shared_task


@shared_task
def update_matching_application():
    User = get_user_model()

    try:
        # 현재 로그인된 사용자를 찾음
        user = User.objects.get(pk=13)

        # matching_application 필드를 0으로 업데이트
        user.matching_application = 0
        user.save()

        # 필요한 추가 작업 수행
        # ...

        return True  # 작업이 성공적으로 완료되었음을 표시
    except User.DoesNotExist:
        return False  # 사용자가 존재하지 않음을 표시