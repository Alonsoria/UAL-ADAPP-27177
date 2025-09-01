import mysql.connector
import csv
from datetime import datetime
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

config_clientes = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'port': 3306,
    'database': 'crm'
}

config_usuarios = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'port': 3306,
    'database': 'dbo'
}

def insertar_datos(cursor, archivo_csv, tabla, columnas, columnas_unicas, formato_fecha="%d/%m/%Y %H:%M"):
    with open(archivo_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # saltar encabezado
        for row in reader:
            datos = list(row)
            # convertir fecha (última columna) a datetime
            if formato_fecha and datos[-1]:
                datos[-1] = datetime.strptime(datos[-1], formato_fecha)

            # FILTRO: solo insertar si el id >= 70
            id_valor = int(datos[0])
            if id_valor < 70:
                continue

            # validación de existencia (ejemplo: email o username)
            condicion = " OR ".join([f"{col} = %s" for col in columnas_unicas])
            valores_unicos = tuple(datos[columnas.index(col)] for col in columnas_unicas)

            cursor.execute(f"SELECT COUNT(*) FROM {tabla} WHERE {condicion}", valores_unicos)
            if cursor.fetchone()[0] == 0:
                placeholders = ", ".join(["%s"] * len(columnas))
                sql = f"INSERT INTO {tabla} ({', '.join(columnas)}) VALUES ({placeholders})"
                cursor.execute(sql, tuple(datos))
            else:
                print(f"Registro con {columnas_unicas}={valores_unicos} ya existe, se omite.")

def main():
    conn_c = cursor_c = None
    try:
        conn_c = mysql.connector.connect(**config_clientes)
        cursor_c = conn_c.cursor()
        insertar_datos(
            cursor_c,
            "clientes.csv",
            tabla="clientes",
            columnas=["cliente_id", "nombre", "apellido", "email", "FechaRegistro"],
            columnas_unicas=["email"]
        )
        conn_c.commit()
        print("Clientes insertados correctamente.")
    except mysql.connector.Error as err:
        print(f"Error clientes: {err}")
        if conn_c:
            conn_c.rollback()
    finally:
        if cursor_c: cursor_c.close()
        if conn_c: conn_c.close()

    conn_u = cursor_u = None
    try:
        conn_u = mysql.connector.connect(**config_usuarios)
        cursor_u = conn_u.cursor()
        insertar_datos(
            cursor_u,
            "usuarios.csv",
            tabla="usuarios",
            columnas=["userId", "username", "first_name", "last_name", "email", "password_hash", "rol", "fecha_creacion"],
            columnas_unicas=["email", "username"]
        )
        conn_u.commit()
        print("Usuarios insertados correctamente.")
    except mysql.connector.Error as err:
        print(f"Error usuarios: {err}")
        if conn_u:
            conn_u.rollback()
    finally:
        if cursor_u: cursor_u.close()
        if conn_u: conn_u.close()

if __name__ == "__main__":
    main()