from django.db import models


class Mailing(models.Model):
    datetime_start = models.DateTimeField()
    text_message = models.TextField()
    client_filter = models.CharField(max_length=255)
    datetime_end = models.DateTimeField()
    is_finish = models.BooleanField(default=False)


class Client(models.Model):
    phone_number = models.CharField(max_length=12)
    operator_code = models.CharField(max_length=5)
    tag = models.CharField(max_length=255)
    time_zone = models.CharField(max_length=255)


class Message(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    send_status = models.CharField(max_length=255)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
