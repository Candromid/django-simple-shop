from django import forms

class CartAddProductForm(forms.Form):
    # поле количества товара (от 1 до 20, по умолчанию 1)
    quantity = forms.IntegerField(
        min_value=1,
        max_value=20,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})  # bootstrap-стиль
    )

    # скрытое поле: заменить количество или прибавить
    override = forms.BooleanField(
        required=False,       # поле необязательное
        initial=False,        # по умолчанию — прибавляем
        widget=forms.HiddenInput()  # не отображается пользователю
    )
