from django import template

#se genero este archivo ya que al trabajar con diccionarios en los templates mo me leia la pk para consultar con ellas los datos del dicccionario

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, None)