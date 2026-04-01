import mysql.connector

cnx = mysql.connector.connect(
    user='openecoe', password='openecoe',    
    host='127.0.0.1',
    port= 8083,
    database='openECOE_dev')

print("Conectado correctamente!")

cnx.close()