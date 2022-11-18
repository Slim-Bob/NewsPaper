from django import template
from ..models import Censorship

register = template.Library()

CURRENCIES_SYMBOLS = {
   'rub': 'Р',
   'usd': '$',
}


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def currency(value, code='rub'):
   """
   value: значение, к которому нужно применить фильтр
   """

   postfix = CURRENCIES_SYMBOLS[code]
   # Возвращаемое функцией значение подставится в шаблон.
   return f'{value} {postfix}'

@register.filter()
def censorship(value:str):
   censorships = Censorship.objects.all().values('pattern')
   r = value
   for pattern in censorships:
      r = r.replace(pattern['pattern'], '***')
   return r