#Esta función introduce en una lista de diccionarios un par clave(=atributo "key")-valorid(=serie_id) 
def introducir_key_id(list_of_dictionary,serie_id, key):
    i = 0
    for dictionary in list_of_dictionary:
        dictionary[key]=serie_id.values[i,0]
        i = i + 1
    return list_of_dictionary
