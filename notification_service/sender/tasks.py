from celery import shared_task


@shared_task(name="check_mailings")
def check_mailings():
    from django.utils import timezone
    from .models import Mailing, Client, Message
    from django.db.models import Q
    from .tasks import sending
    current_date = timezone.now()
    mailings = Mailing.objects.filter(Q(datetime_start__lt=current_date)) \
               & Mailing.objects.filter(Q(datetime_end__gt=current_date)) \
               & Mailing.objects.filter(Q(is_finish=False))

    for mailing in mailings:
        mailing.is_finish = True
        mailing.save()
        clients = Client.objects.filter(Q(operator_code=mailing.client_filter)) | Client.objects.filter(Q(tag=mailing.client_filter))
        messages = []
        for client in clients:
            messages.append(Message(send_status="Sending", mailing=mailing, client=client))
        Message.objects.bulk_create(messages)

    messages = Message.objects.all()
    for message in messages:
        sending.delay(message.id, message.client.phone_number, message.mailing.text_message)


@shared_task(name="sending")
def sending(msgId, phone, text):
    import requests
    import json
    from .models import Message

    url = f'https://probe.fbrq.cloud/v1/send/{msgId}'
    jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTkzMjAyMTcsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Imh0dHBzOi8vdC5tZS9kcmFrc3BsYXkifQ.hHq_CCTqHX5yaQ9zzrLDlcWKY-dpFbB2SICARIUtbI8'  # Замените на ваш JWT-токен

    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json'
    }

    data = {
        "id": msgId,
        "phone": phone,
        "text": text
    }

    response = requests.post(url, headers=headers, data=json.dumps(data)).json()

    if response.get("code") == 0:
        message = Message.objects.get(pk=msgId)
        message.send_status = "Received"
        message.save()

