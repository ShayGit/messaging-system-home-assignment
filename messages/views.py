from django.http import Http404
from rest_framework.viewsets import GenericViewSet
from .models import Message
from .serializers import MessageSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins

from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.


class MessageViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_read']

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def list(self, request, *args, **kwargs):
        messages = self.filter_queryset(self.get_queryset()).filter(receiver=request.user)
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        message = self.get_object()
        if message.receiver == request.user:
            if not message.is_read:
                message.is_read = True
                message.save()
            serializer = self.get_serializer(message)
            return Response(serializer.data)
        raise Http404

    def destroy(self, request, *args, **kwargs):
        message = self.get_object()
        user = request.user
        if message.receiver == user or message.sender == user:
            message.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise Http404
