from .models import Message


def send_message(status, id_mailing, id_client):
    message = Message(send_status=status, mailing=id_mailing, client=id_client)
    message.save()

