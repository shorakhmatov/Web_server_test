from django.core.management.base import BaseCommand
from finance.models import Status, TransactionType, Category, Subcategory

class Command(BaseCommand):
    help = 'Populate initial data for the finance app'

    def handle(self, *args, **kwargs):
        # Create statuses
        statuses = ['Бизнес', 'Личное', 'Налог']
        for status_name in statuses:
            Status.objects.get_or_create(name=status_name)
        self.stdout.write(self.style.SUCCESS('Created statuses'))

        # Create transaction types
        types = ['Пополнение', 'Списание']
        for type_name in types:
            TransactionType.objects.get_or_create(name=type_name)
        self.stdout.write(self.style.SUCCESS('Created transaction types'))

        # Create categories and subcategories
        expense_type = TransactionType.objects.get(name='Списание')
        income_type = TransactionType.objects.get(name='Пополнение')
        
        # Income categories
        income_categories = {
            'Продажи': ['Товары', 'Услуги'],
            'Инвестиции': ['Дивиденды', 'Проценты по вкладам'],
            'Прочие доходы': ['Возврат средств', 'Подарки']
        }
        
        for cat_name, subcats in income_categories.items():
            cat, _ = Category.objects.get_or_create(
                name=cat_name,
                transaction_type=income_type
            )
            for subcat in subcats:
                Subcategory.objects.get_or_create(
                    name=subcat,
                    category=cat
                )
        
        # Expense categories
        
        # Infrastructure category
        infra_cat, _ = Category.objects.get_or_create(
            name='Инфраструктура',
            transaction_type=expense_type
        )
        for subcat in ['VPS', 'Proxy']:
            Subcategory.objects.get_or_create(
                name=subcat,
                category=infra_cat
            )

        # Marketing category
        marketing_cat, _ = Category.objects.get_or_create(
            name='Маркетинг',
            transaction_type=expense_type
        )
        for subcat in ['Farpost', 'Avito']:
            Subcategory.objects.get_or_create(
                name=subcat,
                category=marketing_cat
            )

        self.stdout.write(self.style.SUCCESS('Created categories and subcategories'))
