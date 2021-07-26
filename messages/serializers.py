from rest_framework import serializers
from .models import Message
from django.contrib.auth.models import User


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(read_only=True, slug_field='username')
    receiver = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'subject', 'message', 'is_read', 'creation_date')
        read_only_fields = ('is_read', 'creation_date', 'sender')
