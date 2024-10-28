from typing import Any
from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser

from subscriptions.models import UserSubscription
from customers.models import Customer
import helpers.billing
import subscriptions.utils as subs_utils

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--days-left', default=0, type=int)
        parser.add_argument('--days-ago', default=0, type=int)
        parser.add_argument('--day-start', default=0, type=int)
        parser.add_argument('--day-end', default=0, type=int)
        parser.add_argument('--clear-dangling', action="store_true", default=False)
        parser.add_argument('--sync-active', action="store_true", default=False)


    
    def handle(self, *args, **options):
        days_left = options.get('days_left')
        days_ago = options.get('days_ago')
        clear_dnagling = options.get('clear_dangling')
        sync_active = options.get('sync_active')
        if clear_dnagling:
            print('Clearing Stripe active dangling subs')
            subs_utils.clear_dangling_subs()
            print("Done")
        elif sync_active:
            print('Syncing active subs')
            subs_utils.refresh_users_subscription(active_only=True, days_left=days_left, days_ago=days_ago)
            print("Done")
        else:
            print('Specify one of the possible arguments:')
            print('--clear-dangling')
            print('--sync-active')