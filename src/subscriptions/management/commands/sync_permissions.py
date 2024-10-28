from typing import Any
from django.conf import settings
from django.core.management.base import BaseCommand

from subscriptions.models import Subscription
import subscriptions.utils as subs_utils

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        subs_utils.sync_sub_group_permissions()
