import django_filters
from django import forms
from .models import Transaction, Category, Subcategory

class TransactionFilter(django_filters.FilterSet):
    date_created = django_filters.DateFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'})
    )
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        empty_label="Все категории"
    )
    subcategory = django_filters.ModelChoiceFilter(
        queryset=Subcategory.objects.all(),
        empty_label="Все подкатегории"
    )

    class Meta:
        model = Transaction
        fields = {
            'status': ['exact'],
            'transaction_type': ['exact'],
        }
