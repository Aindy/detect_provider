from django import forms
import re

class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(label='Номер телефона', max_length=12)

    def clean_phone_number(self):
        number = self.cleaned_data['phone_number']

        number = re.sub(r'\D', '', number)
        if not number.isdigit() or len(number) < 7:
            raise forms.ValidationError("Введите корректный номер телефона")
        return number
