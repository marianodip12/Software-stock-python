import sqlite3


class Producto:
    def __init__(self, codigo, nombre, cantidad, precio, minimo):
        self.codigo = codigo
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio
        self.minimo = minimo

    @classmethod
    def crear_manualmente(cls):
        codigo = input("Ingrese el código del producto: ")
        nombre = input("Ingrese el nombre del producto: ")
        cantidad = int(input("Ingrese la cantidad de productos: "))
        precio = float(input("Ingrese el precio del producto: "))
        minimo = int(input("Ingrese la cantidad mínima de productos en stock: "))
        return cls(codigo, nombre, cantidad, precio, minimo)


class Venta:
    def __init__(self, codigo, cantidad, fecha):
        self.codigo = codigo
        self.cantidad = cantidad
        self.fecha = fecha

    @classmethod
    def crear_manualmente(cls):
        codigo = input("Ingrese el código del producto: ")
        cantidad = int(input("Ingrese la cantidad vendida: "))
        fecha = input("Ingrese la fecha de la venta (en formato dd/mm/aaaa): ")
        return cls(codigo, cantidad, fecha)


class Inventario:
    def __init__(self):
        self.conn = sqlite3.connect('inventario.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS productos
                     (codigo TEXT, nombre TEXT, cantidad INTEGER, precio REAL, minimo INTEGER)''')

    def agregar_producto(self, producto):
        self.c.execute("INSERT INTO productos VALUES (?, ?, ?, ?, ?)",
                       (producto.codigo, producto.nombre, producto.cantidad, producto.precio, producto.minimo))
        self.conn.commit()

    def buscar_producto(self, codigo):
        self.c.execute("SELECT * FROM productos WHERE codigo=?", (codigo,))
        producto = self.c.fetchone()
        if producto:
            return Producto(*producto)
        else:
            return None

    def actualizar_cantidad(self, codigo, cantidad):
        self.c.execute("UPDATE productos SET cantidad=? WHERE codigo=?",
                       (cantidad, codigo))
        self.conn.commit()

    def mostrar_inventario(self):
        self.c.execute("SELECT * FROM productos")
        productos = self.c.fetchall()
        if productos:
            print("Código\tNombre\tCantidad\tPrecio\tMínimo")
            for p in productos:
                print("{}\t{}\t{}\t{}\t{}".format(*p))
        else:
            print("No hay productos en stock.")

    def descontar_stock(self, codigo, cantidad):
        producto = self.buscar_producto(codigo)
        if producto:
            nueva_cantidad = producto.cantidad - cantidad
            if nueva_cantidad < 0:
                print("No hay suficiente stock.")
            else:
                self.actualizar_cantidad(codigo, nueva_cantidad)
        else:
            print("Producto no encontrado.")


class Ventas:
    def __init__(self):
        self.conn = sqlite3.connect('ventas.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS ventas
                     (codigo TEXT, cantidad INTEGER, fecha TEXT)''')

    def agregar_venta(self, venta):
        self.c.execute("INSERT INTO ventas VALUES (?, ?, ?)",
                       (venta.codigo, venta.cantidad, venta.fecha))
        self.conn.commit()

    def buscar_venta(self, codigo, fecha):
        self.c.execute("SELECT * FROM ventas WHERE codigo=? AND fecha=?", (codigo, fecha))
        venta = self.c.fetchone()
        if venta:
            return Venta(*venta)
        else:
            return None

def mostrar_ventas(self):
    self.c.execute("SELECT * FROM ventas")
    ventas = self.c.fetchall()
    if ventas:
        print("Código\tCantidad\tFecha")
        for v in ventas:
            print("{}\t{}\t{}".format(*v))
    else:
        print("No hay ventas registradas")


if __name__ == '__main__':
    inventario = Inventario()
    
    while True:
        print("\nMENU")
        print("1 - Inventario")
        print("2 - Ventas")
        print("0 - Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            while True:
                print("\nINVENTARIO")
                print("1 - Agregar un producto")
                print("2 - Mostrar el stock")
                print("0 - Volver")
                opcion_inventario = input("Seleccione una opción: ")
                
                if opcion_inventario == "1":
                    producto = Producto.crear_manualmente()
                    inventario.agregar_producto(producto)
                    print("Producto agregado con éxito.")
                    
                elif opcion_inventario == "2":
                    inventario.mostrar_inventario()
                    
                elif opcion_inventario == "0":
                    break

        elif opcion == "2":
            while True:
                print("\nVENTAS")
                print("1 - Descontar stock por venta")
                print("2 - Mostrar ventas")
                print("3 - Buscar una venta")
                print("0 - Volver")
                opcion_ventas = input("Seleccione una opción: ")
            
                if opcion_ventas == "1":
                    codigo = input("Ingrese el código del producto: ")
                    cantidad = int(input("Ingrese la cantidad vendida: "))
                    inventario.descontar_stock(codigo, cantidad)
                    fecha = input("Ingrese la fecha de la venta (YYYY-MM-DD): ")
                    venta = Venta(codigo, cantidad, fecha)
                    Ventas.agregar_venta(Ventas)
                    print("Stock y ventas actualizados.")
                    
                elif opcion_ventas == "2":
                    Ventas.mostrar_ventas()
                    
                elif opcion_ventas == "3":
                    codigo = input("Ingrese el código del producto: ")
                    fecha = input("Ingrese la fecha de la venta (YYYY-MM-DD): ")
                    venta = Ventas.buscar_venta(codigo, fecha)
                    if venta:
                        print("Cantidad vendida:", venta.cantidad)
                    else:
                        print("Venta no encontrada.")
                    
                elif opcion_ventas == "0":
                    break
                    
                else:
                    print("Opción inválida.")
        
        elif opcion == "0":
            break
        
        else:
            print("Opción inválida.")
