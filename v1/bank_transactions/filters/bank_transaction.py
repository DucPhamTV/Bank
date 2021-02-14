from django.db.models import Q
from django_filters.rest_framework import CharFilter, FilterSet

from ..models.bank_transaction import BankTransaction


class BankTransactionFilter(FilterSet):
    account_number = CharFilter(method='filter_account_number')
    non_fee = CharField(method='filter_non_fee')

    class Meta:
        model = BankTransaction
        fields = [
            'account_number',
            'block__sender',
            'recipient',
            'non_fee',
        ]

    @staticmethod
    def filter_account_number(queryset, _, value):
        """Filter queryset by account number"""
        return queryset.filter(
            Q(block__sender=value)
            | Q(recipient=value)
        )

    @staticmethod
    def filter_non_fee(queryset, _, value):
        """Filter queryset for non-fee transactions"""
        if value == "" or value == "1":
            return queryset.filter(
                fee__exact='',
            )
