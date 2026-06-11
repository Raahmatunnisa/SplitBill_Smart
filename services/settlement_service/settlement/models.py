from django.db import models


class SettlementLog(models.Model):
    bill_id = models.IntegerField()
    result = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Settlement for bill {self.bill_id}'
