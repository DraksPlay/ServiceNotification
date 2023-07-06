from rest_framework import serializers
from .models import Client, Mailing


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = "__all__"


class UpdateClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ["phone_number", "operator_code", "tag", "time_zone"]

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        instance.operator_code = validated_data.get("operator_code", instance.operator_code)
        instance.tag = validated_data.get("tag", instance.tag)
        instance.time_zone = validated_data.get("time_zone", instance.time_zone)
        instance.save()
        return instance


class MailingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mailing
        fields = ["datetime_start", "text_message", "client_filter", "datetime_end"]


class UpdateMailingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mailing
        fields = ["datetime_start", "text_message", "client_filter", "datetime_end"]

    def update(self, instance, validated_data):
        instance.datetime_start = validated_data.get("datetime_start", instance.datetime_start)
        instance.text_message = validated_data.get("text_message", instance.text_message)
        instance.client_filter = validated_data.get("client_filter", instance.client_filter)
        instance.datetime_end = validated_data.get("datetime_end", instance.datetime_end)
        instance.save()
        return instance
