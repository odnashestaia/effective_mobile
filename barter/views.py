from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Ad, ExchangeProposal
from .serializers import AdSerializer, ExchangeProposalSerializer


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all().order_by("-created_at")
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["category", "condition"]
    search_fields = ["title", "description"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if self.get_object().user != self.request.user:
            raise PermissionDenied("Вы не автор этого объявления.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("Вы не автор этого объявления.")
        instance.delete()


class ExchangeProposalViewSet(viewsets.ModelViewSet):
    queryset = ExchangeProposal.objects.all().order_by("-created_at")
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["ad_sender", "ad_receiver", "status"]

    def perform_create(self, serializer):
        serializer.save(status="pending")

    @action(detail=True, methods=["post"])
    def accept(self, request, pk=None):
        proposal = self.get_object()
        if proposal.ad_receiver.user != request.user:
            raise PermissionDenied("Вы не можете принять это предложение.")
        proposal.status = "accepted"
        proposal.save()
        return Response({"status": "accepted"})

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        proposal = self.get_object()
        if proposal.ad_receiver.user != request.user:
            raise PermissionDenied("Вы не можете отклонить это предложение.")
        proposal.status = "rejected"
        proposal.save()
        return Response({"status": "rejected"})
