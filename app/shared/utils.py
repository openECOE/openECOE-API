from decimal import Decimal
from flask import json

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)

def order_items(item, items, new_order, operation):
    # Posibles operaciones add y del (añadir y borrar)
    # Los items del array tienen que tener la propiedad order
    if new_order < 1:
        item.order = 1
    else:
        item_idx = item.order - 1
        if operation == 'add':
            position = new_order - 1
            if new_order > len(items):
                position = len(items)
                
            items.insert(position, items.pop(item_idx))
        else:
            items.pop(item_idx)
        
    calculate_order(items)

def calculate_order(items):
    for idx, current_item in enumerate(items):
        current_item.order = idx + 1