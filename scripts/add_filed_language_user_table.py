import mysql.connector
from mysql.connector import Error

try:
    # 1. Establecer la conexión
    cnx = mysql.connector.connect(
        user='openecoe', 
        password='openecoe',    
        host='127.0.0.1',
        port=8083,
        database='openECOE_dev'
    )

    if cnx.is_connected():
        print("Conectado correctamente!")
        
        # 2. Crear el objeto cursor
        cursor = cnx.cursor()

        # 3. Definir y ejecutar la sentencia SQL
        sql_alter = "ALTER TABLE user ADD COLUMN language ENUM('es', 'en', 'va') NOT NULL DEFAULT 'es';"
        
        try:
            cursor.execute(sql_alter)
            print("Campo 'language' creado con éxito.")
        except Error as e:
            print(f"Error al modificar la tabla: {e}")

except Error as e:
    print(f"Error al conectar a la base de datos: {e}")

finally:
    # 4. Cerrar cursor y conexión
    if 'cursor' in locals():
        cursor.close()
    if 'cnx' in locals() and cnx.is_connected():
        cnx.close()
        print("Conexión cerrada.")