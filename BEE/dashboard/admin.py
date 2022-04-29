from django.contrib import admin

from dashboard.models import (
    AccountIncomingMailStats,
    AccountOutgoingMailStats,
    ConnectedAccount,
    IntegratedAccount,
)

admin.site.register(AccountIncomingMailStats)
admin.site.register(AccountOutgoingMailStats)
admin.site.register(ConnectedAccount)
admin.site.register(IntegratedAccount)
