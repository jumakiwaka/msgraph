from django.contrib.auth.models import User
from django.db import models


class ConnectedAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    email = models.CharField(blank=False, null=False, max_length=255, default="")
    access_token = models.TextField(blank=False, null=False, default="")
    refresh_token = models.TextField(blank=False, null=True, default=None)
    access_token_expire_date = models.DateTimeField(
        blank=False, null=True, default=None
    )
    refresh_token_expire_date = models.DateTimeField(
        blank=False, null=True, default=None
    )
    is_sync_running = models.BooleanField(blank=False, null=False, default=False)
    is_sync_completed = models.BooleanField(blank=False, null=False, default=False)
    last_job_run = models.DateTimeField(blank=False, null=True, default=None)

    def __str__(self):
        return str(self.email)


class IntegratedAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    connected_account = models.ForeignKey(
        ConnectedAccount, on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return str(self.connected_account.email)


class AccountIncomingMailStats(models.Model):
    connected_account = models.ForeignKey(ConnectedAccount, on_delete=models.CASCADE, null=True)
    conversation_id = models.TextField(blank=False, null=False, default="")
    message_id = models.TextField(blank=False, null=False, default="")
    sent_date_time = models.DateTimeField(null=True, blank=False, default=None)
    is_read = models.BooleanField(blank=False, null=False, default=False)
    is_read_date_time = models.DateTimeField(null=True, blank=False, default=None)
    # read_time_difference = models.IntegerField(null=True, blank=False, default=None)
    read_time_taken = models.FloatField(null=True, blank=False, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.account.email)


class AccountOutgoingMailStats(models.Model):
    connected_account = models.ForeignKey(ConnectedAccount, on_delete=models.CASCADE, null=True)
    conversation_id = models.TextField(blank=False, null=False, default="")
    message_id = models.TextField(blank=False, null=False, default="")
    sent_date_time = models.DateTimeField(null=True, blank=False, default=None)
    inbox_email = models.ForeignKey(
        AccountIncomingMailStats, on_delete=models.CASCADE, null=True
    )
    response_time = models.IntegerField(null=True, blank=False, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.account.email)
