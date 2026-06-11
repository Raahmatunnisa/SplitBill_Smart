from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='members')
    user_id = models.IntegerField()
    username = models.CharField(max_length=150, blank=True, default='')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('group', 'user_id')

    def __str__(self):
        return f'{self.username or self.user_id} in {self.group.name}'
