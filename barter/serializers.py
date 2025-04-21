from rest_framework import serializers

from .models import Ad, ExchangeProposal


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at"]


class ExchangeProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeProposal
        fields = "__all__"
        read_only_fields = ["id", "status", "created_at"]
