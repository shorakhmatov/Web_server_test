from django.core.management.base import BaseCommand
from django.utils import timezone
from finance.models import Status, TransactionType, Category, Subcategory, Transaction
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Populate database with test transactions'

    def handle(self, *args, **options):
        # Получаем существующие записи
        statuses = list(Status.objects.all())
        types = list(TransactionType.objects.all())
        categories = list(Category.objects.all())
        subcategories = list(Subcategory.objects.all())

        if not all([statuses, types, categories, subcategories]):
            self.stdout.write('Сначала нужно выполнить команду populate_initial_data')
            return

        # Создаем тестовые транзакции
        test_transactions = [
            {
                'date_created': timezone.now().date(),
                'status': random.choice(statuses),
                'transaction_type': types[0],  # Доход
                'category': categories[0],
                'subcategory': subcategories[0],
                'amount': Decimal('150000.00'),
                'comment': 'Зарплата за апрель'
            },
            {
                'date_created': timezone.now().date(),
                'status': random.choice(statuses),
                'transaction_type': types[1],  # Расход
                'category': categories[1],
                'subcategory': subcategories[1],
                'amount': Decimal('45000.00'),
                'comment': 'Продукты на неделю'
            },
            {
                'date_created': timezone.now().date(),
                'status': random.choice(statuses),
                'transaction_type': types[1],  # Расход
                'category': categories[2],
                'subcategory': subcategories[2],
                'amount': Decimal('25000.00'),
                'comment': 'Оплата интернета'
            },
            {
                'date_created': timezone.now().date(),
                'status': random.choice(statuses),
                'transaction_type': types[0],  # Доход
                'category': categories[0],
                'subcategory': subcategories[0],
                'amount': Decimal('50000.00'),
                'comment': 'Премия'
            },
            {
                'date_created': timezone.now().date(),
                'status': random.choice(statuses),
                'transaction_type': types[1],  # Расход
                'category': categories[3],
                'subcategory': subcategories[3],
                'amount': Decimal('15000.00'),
                'comment': 'Развлечения'
            }
        ]

        # Сохраняем транзакции
        for transaction_data in test_transactions:
            Transaction.objects.create(**transaction_data)
            self.stdout.write(f'Создана транзакция на сумму {transaction_data["amount"]} руб.')

        self.stdout.write(self.style.SUCCESS('Тестовые транзакции успешно созданы'))
