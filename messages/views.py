from django.http import Http404
from rest_framework.viewsets import GenericViewSet
from .models import Message
from .serializers import MessageSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins


# Create your views here.


class MessageViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        messages = Message.objects.all()
        return messages

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user, receiver=serializer.validated_data['receiver'])

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(receiver=request.user)
        unread = request.query_params.get('unread', None)
        messages = queryset
        if unread is not None:
            if unread == 'true':
                messages = messages.filter(is_read=False)
            elif unread == 'false':
                messages = messages.filter(is_read=True)
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
