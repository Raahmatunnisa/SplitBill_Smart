from django.db import models


class Bill(models.Model):
    group_id = models.IntegerField()
    title = models.CharField(max_length=200)
    created_by = models.IntegerField()
    created_by_username = models.CharField(max_length=150, blank=True, default='')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def recalculate_total(self):
        total = sum(item.price for item in self.items.all())
        self.total_amount = total
        self.save(update_fields=['total_amount'])


class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    consumed_by_user_ids = models.JSONField(default=list)

    def __str__(self):
        return f'{self.item_name} - {self.price}'
