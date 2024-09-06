from django import template

register = template.Library()

@register.filter
def get_quantite_field(cleaned_data, consommable):
    field_name = f"quantite_{consommable.id}"
    return cleaned_data.get(field_name, 0)  # Renvoie la quantité ou 0 par défaut
