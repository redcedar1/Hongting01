from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 프로젝트 설정을 사용하도록 설정합니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Celery 애플리케이션을 생성합니다.
app = Celery('myproject')

# Celery 앱 설정을 로드합니다.
app.config_from_object('django.conf:settings', namespace='CELERY')

# 등록된 task를 모두 찾아서 자동으로 task로 등록합니다.
app.autodiscover_tasks()