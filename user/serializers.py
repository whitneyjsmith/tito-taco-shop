from rest_framework import serializers
from user.models import User
from ledger.models import TacoBank


class UserSerializer(serializers.ModelSerializer):

    taco_balance = serializers.SerializerMethodField()

    @classmethod
    def get_taco_balance(csl, user) -> int:
        return TacoBank.objects.get_or_create(user=user)[0].total_tacos if user.is_authenticated else 0

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'unique_id', 'taco_balance')