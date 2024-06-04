from rest_framework import viewsets
from rest_framework.response import Response

from .models import Card
from .serializers import CardSerializer


class CardViewSet(viewsets.ModelViewSet):

    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def list(self, request, **args):
        current_user = request.user
        title = request.query_params.get('title')
        user_cards = Card.objects.filter(user=current_user.id).order_by('-created_at')
        serializer = CardSerializer(user_cards, many=True)
        if title:
            user_cards = Card.objects.filter(user=current_user.id, title=title)
            serializer = CardSerializer(user_cards, many=True)

        return Response(serializer.data)