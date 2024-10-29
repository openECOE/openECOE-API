import pandas as pd
from app.model import db

#Suplementary functions used by some jobs related to the statistics module.

#Used by the endpoint Csv
#This function inserts a key-value pair in each of the dicts inside a list.
#key is taken as a parameter
#The value inserted into each dict is taken from a Pandas serie
def introducir_key_id(list_of_dictionary,serie_id, key):
    i = 0
    for dictionary in list_of_dictionary:
        dictionary[key]=serie_id.values[i,0]
        i = i + 1
    return list_of_dictionary