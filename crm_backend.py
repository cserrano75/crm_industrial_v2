from database import obtener_conexion

class GestorClientes:
    """Clase encargada EXCLUSIVAMENTE de hablar con MySQL"""
    
    @staticmethod
    def listar():
        con = obtener_conexion()
        if con:
            cursor = con.cursor()
            cursor.execute("SELECT id, nombre, empresa FROM clientes")
            datos = cursor.fetchall()
            con.close()
            return datos
        return []

    @staticmethod
    def guardar(nombre, empresa):
        con = obtener_conexion()
        if con:
            cursor = con.cursor()
            sql = "INSERT INTO clientes (nombre, empresa) VALUES (%s, %s)"
            cursor.execute(sql, (nombre, empresa))
            con.commit()
            con.close()
            return True
        return False

    @staticmethod
    def borrar(id_cliente):
        con = obtener_conexion()
        if con:
            cursor = con.cursor()
            cursor.execute("DELETE FROM clientes WHERE id = %s", (id_cliente,))
            con.commit()
            con.close()
            return True
        return False

    @staticmethod
    def obtener_uno(id_cliente):
        con = obtener_conexion()
        if con:
            cursor = con.cursor()
            cursor.execute("SELECT nombre, empresa FROM clientes WHERE id = %s", (id_cliente,))
            res = cursor.fetchone()
            con.close()
            return res
        return None

    @staticmethod
    def actualizar(id_cliente, nombre, empresa):
        con = obtener_conexion()
        if con:
            cursor = con.cursor()
            cursor.execute("UPDATE clientes SET nombre=%s, empresa=%s WHERE id=%s", (nombre, empresa, id_cliente))
            con.commit()
            con.close()
            return True
        return False