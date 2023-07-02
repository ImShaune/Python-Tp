import time
import os
import sqlite3

# Verificar si el archivo de la base de datos existe
if not os.path.exists("comercio.sqlite"):
    # Crear la conexión a la base de datos y el archivo si no existe
    conn = sqlite3.connect("comercio.sqlite")
    conn.close()

# Configuración SQLite
conn = sqlite3.connect("comercio.sqlite")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS registro (id INT, encargado TEXT, fecha TEXT, evento TEXT, caja REAL)")
cursor.execute("CREATE TABLE IF NOT EXISTS ventas (id INT, cliente TEXT, fecha TEXT, combo_S INT, combo_D INT, combo_T INT, flurby INT, total REAL)")

# Definición de variables
caja_encargado = 0
encargadoactual = ""

# Definición de funciones

def incrementar_ingreso():
    cursor.execute("SELECT MAX(id) FROM registro")
    max_id = cursor.fetchone()[0]
    if max_id is not None:
        return max_id + 1
    else:
        return 1

def incrementar_venta():
    cursor.execute("SELECT MAX(id) FROM ventas")
    max_id = cursor.fetchone()[0]
    if max_id is not None:
        return max_id + 1
    else:
        return 1

def ingresar_opcion():
    global encargadoactual
    print("\nBienvenido a Hamburguesas IT")
    print("Encargad@ ->", encargadoactual)
    print("Recuerda, siempre hay que recibir al cliente con una sonrisa :)\n")
    print("##### MENU #####")
    print("1 - Ingresar nuevo pedido")
    print("2 - Cambio de turno")
    print("3 - Apagar sistema")
    opcion = input("Ingrese la opción que desea ejecutar: \n--> ")
    print("############################################")
    return opcion

def ingresar_pedido():
    global encargadoactual, caja_encargado

    nombre_cliente = input("Ingrese nombre del cliente: ")
    while not nombre_cliente.isalpha():
        print("La información ingresada no es válida. Por favor, ingrese solo letras.")
        nombre_cliente = input("Ingrese nombre del cliente: ")

    cantidad_combo_s = ingresar_cantidad("Combo S")
    cantidad_combo_d = ingresar_cantidad("Combo D")
    cantidad_combo_t = ingresar_cantidad("Combo T")
    cantidad_flurby = ingresar_cantidad("Flurby")

    total = (cantidad_combo_s * 5) + (cantidad_combo_d * 6) + (cantidad_combo_t * 7) + (cantidad_flurby * 2)
    print("Total a pagar: $", total)

    pago = ingresar_monto("monto del cliente")
    vuelto = pago - total
    print("El vuelto es: $", vuelto)

    confirmar = input("¿Confirmar pedido? Y/N \n--> ")
    while confirmar.lower() not in ["y", "n"]:
        print("Opción inválida. Ingrese 'Y' para confirmar o 'N' para cancelar.")
        confirmar = input("¿Confirmar pedido? Y/N \n--> ")

    if confirmar.lower() == "y":
        print("Pedido confirmado")
        caja_encargado += total
        guardar_venta(nombre_cliente, cantidad_combo_s, cantidad_combo_d, cantidad_combo_t, cantidad_flurby, total)
    else:
        print("Pedido cancelado")

def ingresar_cantidad(item):
    while True:
        cantidad = input(f"Ingrese cantidad de {item}: ")
        if not cantidad.isdecimal():
            print("El valor ingresado no es válido. Por favor, ingrese un número entero.")
        else:
            return int(cantidad)

def ingresar_monto(mensaje):
    while True:
        monto = input(f"Ingrese {mensaje}: ")
        try:
            monto = float(monto)
            return monto
        except ValueError:
            print("La entrada no es un número válido. Ingréselo de nuevo.")

def guardar_ingreso():
    global encargadoactual, caja_encargado
    id_ingreso = incrementar_ingreso()
    cursor.execute("INSERT INTO registro VALUES (?, ?, ?, ?, ?)", (id_ingreso, encargadoactual, time.asctime(), 'IN', caja_encargado))
    conn.commit()

def guardar_egreso():
    global encargadoactual, caja_encargado
    id_egreso = incrementar_ingreso()
    cursor.execute("INSERT INTO registro VALUES (?, ?, ?, ?, ?)", (id_egreso, encargadoactual, time.asctime(), 'OUT', caja_encargado))
    conn.commit()

def guardar_venta(cliente, combo_s, combo_d, combo_t, flurby, total):
    id_venta = incrementar_venta()
    cursor.execute("INSERT INTO ventas VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (id_venta, cliente, time.asctime(), combo_s, combo_d, combo_t, flurby, total))
    conn.commit()

def main():
    os.system("cls" if os.name == "nt" else "clear")
    print("Bienvenido a Hamburguesas IT")
    encargadoactual = input("Ingrese su nombre, encargad@: \n--> ")
    guardar_ingreso()

    while True:
        opcion = ingresar_opcion()

        if opcion == "1":
            os.system("cls" if os.name == "nt" else "clear")
            ingresar_pedido()
        elif opcion == "2":
            guardar_egreso()
            os.system("cls" if os.name == "nt" else "clear")
            print("Bienvenido a Hamburguesas IT")
            encargadoactual = input("Ingrese su nombre, encargad@: \n--> ")
            guardar_ingreso()
        elif opcion == "3":
            break
        else:
            print("La opción ingresada no es válida, inténtelo de nuevo")

    os.system("cls" if os.name == "nt" else "clear")
    print("Saliendo de la aplicación...\n¡Gracias por usarla!")

if __name__ == "__main__":
    main()

conn.close()
