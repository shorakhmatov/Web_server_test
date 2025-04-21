from django import forms
from .models import Transaction, Category, Subcategory

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date_created', 'status', 'transaction_type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'date_created': forms.DateInput(attrs={'type': 'date'}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategories.all()
        else:
            self.fields['subcategory'].queryset = Subcategory.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')

        if transaction_type and category:
            if category.transaction_type != transaction_type:
                raise forms.ValidationError(
                    'Категория не соответствует выбранному типу транзакции'
                )

        if category and subcategory:
            if subcategory.category != category:
                raise forms.ValidationError(
                    'Подкатегория не соответствует выбранной категории'
                )

        return cleaned_data

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'transaction_type']

class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name', 'category']
