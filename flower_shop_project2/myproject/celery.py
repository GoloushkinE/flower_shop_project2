import os
from celery import Celery

# Задаем переменную окружения, чтобы celery знала где искать настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')

# Используем наш файл настроек
app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery будет автоматически искать задачи в файлах tasks.py наших приложений
app.autodiscover_tasks()