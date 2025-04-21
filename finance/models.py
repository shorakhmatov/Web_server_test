from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Statuses'

class TransactionType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE, related_name='categories')
    
    def __str__(self):
        return f'{self.name} ({self.transaction_type.name})'
    
    class Meta:
        verbose_name_plural = 'Categories'

class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    
    def __str__(self):
        return f'{self.name} ({self.category.name})'
    
    class Meta:
        verbose_name_plural = 'Subcategories'

class Transaction(models.Model):
    date_created = models.DateField(default=timezone.now)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    comment = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.date_created} - {self.transaction_type.name} - {self.amount} руб.'
