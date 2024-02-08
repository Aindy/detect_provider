from django.shortcuts import render
from telecom.forms import PhoneNumberForm
from telecom.models import PhoneNumber

def index(request):
    context = {'form': PhoneNumberForm(), 'result': None, 'error': None}

    if request.method == 'POST':
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data['phone_number']
            try:
                number_int = int(number[-7:])
                phone_number = PhoneNumber.objects.filter(start_range__lte=number_int, end_range__gte=number_int).first()
                if phone_number:
                    context['result'] = {
                        'number': number,
                        'operator': phone_number.operator.name,
                        'region': phone_number.region
                    }
                else:
                    context['error'] = 'Номер не найден'
            except ValueError:
                context['error'] = 'Неверный формат номера'
        else:
            context['error'] = form.errors.as_text()
    else:
        context['form'] = PhoneNumberForm()

    return render(request, 'index.html', context)
