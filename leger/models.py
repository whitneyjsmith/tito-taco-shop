from django.db import models
from datetime import date
from django.db.models import Sum


class User(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField()
    creation_date = models.DateField(default=date.today())
    is_active = models.BooleanField(default=True)
    unique_id = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'unique_id'],
                name='Taco Shop User Model'
            )
        ]

    def __str__(self):
        return f'{self.first_name} {self.last_name}, {self.email}'


class TacoLedger(models.Model):
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    receiver = models.CharField(max_length=100)
    giver = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.timestamp}: {self.giver} --> {self.receiver}, {self.amount} tacos'


class TacoBank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                name='Taco Shop Bank'
            )
        ]

    def __str__(self):
        return f'Bank: {self.user}, amount: {self.total}'

    @property
    def total_given(self):
        return TacoLedger.objects.filter(giver=self.user.unique_id).aggregate(Sum('amount'))

    @property
    def total_received(self):
        return TacoLedger.objects.filter(receiver=self.user.unique_id).aggregate(Sum('amount'))

    @property
    def total_redeemed(self):
        return TacoLedger.objects.filter(giver=self.user.unique_id, reciever='666').aggregate(Sum('amount'))

    @property
    def total_tacos(self):
        amount = (self.total_given + self.total_received) - self.total_redeemed
        return amount if amount > 0 else 0


