def order_items(item, items, new_order, operation):
    # Posibles operaciones add y del (añadir y borrar)
    # Los items del array tienen que tener la propiedad order
    if item.order > len(items) or item.order < 1:
        item.order = len(items)
    else:
        item_idx = item.order - 1
        if operation == 'add':
            items.insert(new_order - 1, items.pop(item_idx))
        else:
            items.pop(item_idx)
        
        calculate_order(items)

def calculate_order(items):
    for idx, current_item in enumerate(items):
        current_item.order = idx + 1