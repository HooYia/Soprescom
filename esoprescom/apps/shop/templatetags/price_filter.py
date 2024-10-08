from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='format_price')
@stringfilter
def format_price(value):
  try:
      value = float(value)

      return  '{:.2f} FCFA'.format(value)
  except :
      return value


@register.filter(name='solde_rate')
def solde_rate(product):
  try:
      solde_price = float(product.solde_price)
      regular_price = float(product.regular_price)
      rate = ((regular_price - solde_price )/regular_price)*100

      return  f"{int(rate)}% off"
  except Exception as e:
      print(e)
      return   f"{0}% off"