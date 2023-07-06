import os
from celery import Celery

# Установите переменную окружения для указания настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notification_service.settings')

# Создайте экземпляр объекта Celery
app = Celery('notification_service')

# Загрузите настройки из файла `settings.py`
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое определение и регистрация задач из файлов `tasks.py` в приложениях Django
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'checker_second': {
        'task': 'check_mailings',
        'schedule': 60.0,
    },
}
