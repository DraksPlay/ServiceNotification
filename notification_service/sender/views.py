from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Client, Mailing, Message
from .serializers import ClientSerializer, UpdateClientSerializer, MailingSerializer, UpdateMailingSerializer
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(method='POST', request_body=ClientSerializer, tags=["Client"])
@api_view(['POST'])
def create_client(request):
    if request.method == 'POST':
        create_client = ClientSerializer(data=request.data)
        if create_client.is_valid():
            phone_number = create_client.validated_data.get('phone_number')
            operator_code = create_client.validated_data.get('operator_code')
            tag = create_client.validated_data.get('tag')
            time_zone = create_client.validated_data.get('time_zone')
            client = Client.objects.create(phone_number=phone_number, operator_code=operator_code,
                                           tag=tag, time_zone=time_zone)
            client.save()
            return Response(create_client.data, status=status.HTTP_201_CREATED)
        else:
            return Response(create_client.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Error": "Invalid request type"}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='GET', tags=["Client"])
@api_view(['GET'])
def read_client(request, *args, **kwargs):
    if kwargs.get("id"):
        try:
            client = Client.objects.get(id=kwargs.get("id"))
            serialized_clients = ClientSerializer(client)
        except Exception as e:
            return Response({"Error": f"Unexpected error {e} occurred."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        all_clients = Client.objects.all()
        serialized_clients = ClientSerializer(all_clients, many=True)
    if request.method == 'GET':
        return Response(serialized_clients.data, status=status.HTTP_200_OK)
    else:
        return Response(serialized_clients.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='PATCH', request_body=UpdateClientSerializer, tags=["Client"])
@api_view(['PATCH'])
def update_client(request, id):
    if request.method == 'PATCH':
        try:
            client = Client.objects.get(id=id)
            update_serializer = UpdateClientSerializer(client, data=request.data, partial=True)
            if update_serializer.is_valid():
                update_serializer.save()
                return Response({"Message": "Client updated"}, status=status.HTTP_200_OK)
            else:
                return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error": f"Unexpected error {e} occurred."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Error": "Invalid request type"}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='DELETE', tags=["Client"])
@api_view(['DELETE'])
def delete_client(request, id):
    if request.method == 'DELETE':
        try:
            client = Client.objects.get(id=id)
            client.delete()
        except Exception as e:
            return Response({"Error": f"Unexpected error {e} occurred."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Message": "Client have been deleted"}, status=status.HTTP_200_OK)
    else:
        return Response({"Error": "Invalid request type"}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='POST', request_body=MailingSerializer, tags=["Mailing"])
@api_view(['POST'])
def create_mailing(request):
    if request.method == 'POST':
        create_mailing = MailingSerializer(data=request.data)
        if create_mailing.is_valid():
            datetime_start = create_mailing.validated_data.get('datetime_start')
            text_message = create_mailing.validated_data.get('text_message')
            client_filter = create_mailing.validated_data.get('client_filter')
            datetime_end = create_mailing.validated_data.get('datetime_end')
            mailing = Mailing.objects.create(datetime_start=datetime_start, text_message=text_message,
                                             client_filter=client_filter, datetime_end=datetime_end)
            mailing.save()
            return Response(create_mailing.data, status=status.HTTP_201_CREATED)
        else:
            return Response(create_client.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Error": "Invalid request type"}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='PATCH', request_body=UpdateMailingSerializer, tags=["Mailing"])
@api_view(['PATCH'])
def update_mailing(request, id):
    if request.method == 'PATCH':
        try:
            mailing = Mailing.objects.get(id=id)
            update_serializer = UpdateMailingSerializer(mailing, data=request.data, partial=True)
            if update_serializer.is_valid():
                update_serializer.save()
                return Response({"Message": "Mailing updated"}, status=status.HTTP_200_OK)
            else:
                return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error": f"Unexpected error {e} occurred."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Error": "Invalid request type"}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='DELETE', tags=["Mailing"])
@api_view(['DELETE'])
def delete_mailing(request, id):
    if request.method == 'DELETE':
        try:
            mailing = Mailing.objects.get(id=id)
            mailing.delete()
        except Exception as e:
            return Response({"Error": f"Unexpected error {e} occurred."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Message": "Mailing have been deleted"}, status=status.HTTP_200_OK)
    else:
        return Response({"Error": "Invalid request type"}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='GET', tags=["Mailing"])
@api_view(['GET'])
def read_mailing(request, *args, **kwargs):
    if kwargs.get("id"):
        all_messages = Message.objects.filter(mailing_id=kwargs.get("id")).count()
        received_messages = (Message.objects.filter(send_status="Received") & Message.objects.filter(mailing_id=kwargs.get("id"))).count()
    else:
        all_messages = Message.objects.all().count()
        received_messages = Message.objects.filter(send_status="Received").count()
    resp_data = {"all_messages": all_messages, "received_messages": received_messages}
    if request.method == 'GET':
        return Response(resp_data, status=status.HTTP_200_OK)
    else:
        return Response(resp_data, status=status.HTTP_400_BAD_REQUEST)