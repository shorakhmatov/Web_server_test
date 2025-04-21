from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import models
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from .models import Transaction, Category, Subcategory, Status, TransactionType
from .forms import TransactionForm, CategoryForm, SubcategoryForm
from .filters import TransactionFilter

@method_decorator(ensure_csrf_cookie, name='dispatch')
class TransactionListView(ListView):
    model = Transaction
    template_name = 'finance/transaction_list.html'
    context_object_name = 'transactions'
    ordering = ['-date_created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filtered_qs = TransactionFilter(self.request.GET, queryset=self.get_queryset())
        context['filter'] = filtered_qs
        
        # Calculate totals for income and expense
        income_sum = filtered_qs.qs.filter(transaction_type__name='Пополнение').aggregate(total=models.Sum('amount'))['total'] or 0
        expense_sum = filtered_qs.qs.filter(transaction_type__name='Списание').aggregate(total=models.Sum('amount'))['total'] or 0
        
        context.update({
            'income_total': income_sum,
            'expense_total': expense_sum,
            'balance': income_sum - expense_sum
        })
        return context
        
    def get_ordering(self):
        # Get the sort parameter from request GET parameters
        sort = self.request.GET.get('sort')
        if sort in ['date_created', '-date_created', 'amount', '-amount']:
            return [sort]
        return ['-date_created']  # default sorting

    def get_queryset(self):
        queryset = super().get_queryset()
        return TransactionFilter(self.request.GET, queryset=queryset).qs

@method_decorator(ensure_csrf_cookie, name='dispatch')
class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'finance/transaction_form.html'
    success_url = reverse_lazy('transaction_list')

    def form_valid(self, form):
        messages.success(self.request, 'Транзакция успешно создана')
        return super().form_valid(form)

class TransactionUpdateView(UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'finance/transaction_form.html'
    success_url = reverse_lazy('transaction_list')

    def form_valid(self, form):
        messages.success(self.request, 'Транзакция успешно обновлена')
        return super().form_valid(form)

class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = 'finance/transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Транзакция успешно удалена')
        return super().delete(request, *args, **kwargs)

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)

def get_categories(request):
    """AJAX view to get categories for a given transaction type.
    
    Returns categories filtered by transaction type ID from GET parameters.
    """
    type_id = request.GET.get('type_id')
    categories = Category.objects.filter(transaction_type_id=type_id).values('id', 'name')
    return JsonResponse(list(categories), safe=False)

@method_decorator(ensure_csrf_cookie, name='dispatch')
class ReferenceListView(ListView):
    template_name = 'finance/reference_list.html'
    model = Status  # Используем любую модель, так как нам нужен только шаблон
    
    def get_queryset(self):
        # Возвращаем пустой QuerySet, так как мы не используем его
        return Status.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'statuses': Status.objects.all(),
            'types': TransactionType.objects.all(),
            'categories': Category.objects.all(),
            'subcategories': Subcategory.objects.all(),
        })
        return context
        
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', 'create')
        item_type = request.POST.get('item_type')
        
        if action == 'create':
            name = request.POST.get('name')
            
            if not name:
                messages.error(request, 'Необходимо указать название')
                return redirect('reference_list')
                
            try:
                if item_type == 'status':
                    Status.objects.create(name=name)
                elif item_type == 'type':
                    TransactionType.objects.create(name=name)
                elif item_type == 'category':
                    transaction_type_id = request.POST.get('transaction_type')
                    if not transaction_type_id:
                        messages.error(request, 'Необходимо выбрать тип операции')
                        return redirect('reference_list')
                    transaction_type = get_object_or_404(TransactionType, id=transaction_type_id)
                    Category.objects.create(name=name, transaction_type=transaction_type)
                elif item_type == 'subcategory':
                    category_id = request.POST.get('category')
                    if not category_id:
                        messages.error(request, 'Необходимо выбрать категорию')
                        return redirect('reference_list')
                    category = get_object_or_404(Category, id=category_id)
                    Subcategory.objects.create(name=name, category=category)
                
                messages.success(request, 'Элемент успешно создан')
            except Exception as e:
                messages.error(request, f'Ошибка при создании элемента: {str(e)}')
        
        elif action == 'delete':
            item_id = request.POST.get('item_id')
            try:
                if item_type == 'status':
                    Status.objects.filter(id=item_id).delete()
                elif item_type == 'type':
                    TransactionType.objects.filter(id=item_id).delete()
                elif item_type == 'category':
                    Category.objects.filter(id=item_id).delete()
                elif item_type == 'subcategory':
                    Subcategory.objects.filter(id=item_id).delete()
                messages.success(request, 'Элемент успешно удален')
            except Exception as e:
                messages.error(request, f'Ошибка при удалении элемента: {str(e)}')

        elif action == 'edit':
            item_id = request.POST.get('item_id')
            name = request.POST.get('name')
            try:
                if item_type == 'status':
                    item = Status.objects.get(id=item_id)
                elif item_type == 'type':
                    item = TransactionType.objects.get(id=item_id)
                elif item_type == 'category':
                    item = Category.objects.get(id=item_id)
                elif item_type == 'subcategory':
                    item = Subcategory.objects.get(id=item_id)
                
                if name:
                    item.name = name
                    item.save()
                    messages.success(request, 'Элемент успешно обновлен')
            except Exception as e:
                messages.error(request, f'Ошибка при обновлении элемента: {str(e)}')

        return redirect('reference_list')
