from django.contrib import admin
from .models import TacoLedger, TacoBank


# Register your models here.
@admin.register(TacoLedger)
class TacoLedgerAdmin(admin.ModelAdmin):
    pass


@admin.register(TacoBank)
class TacoBankAdmin(admin.ModelAdmin):
    pass