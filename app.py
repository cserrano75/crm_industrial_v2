import customtkinter as ctk
from database import obtener_conexion 

class AppCRM(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. Configuración de la Ventana
        self.title("Sistema de Gestión B2B - CRM")
        self.geometry("800x450")
        ctk.set_appearance_mode("light")

        # 2. Diseño del Layout (Grid)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 3. Menú Lateral
        self.menu_lateral = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.menu_lateral.grid(row=0, column=0, sticky="nsew")
        
        self.lbl_logo = ctk.CTkLabel(self.menu_lateral, text="CRM DE GESTION", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_logo.pack(pady=20)

        # BOTONES DEL MENÚ: Ahora llaman a las funciones correctas
        self.btn_listar = ctk.CTkButton(self.menu_lateral, text="Listar Clientes", command=self.mostrar_tabla)
        self.btn_listar.pack(padx=20, pady=10)

        self.btn_nuevo = ctk.CTkButton(self.menu_lateral, text="Nuevo Registro", command=self.mostrar_formulario)
        self.btn_nuevo.pack(padx=20, pady=10)

        self.btn_borrar = ctk.CTkButton(self.menu_lateral, text="Borrar Cliente", fg_color="#A30000", hover_color="#7A0000",command=self.eliminar_cliente)
        self.btn_borrar.pack(padx=20, pady=10)

        self.btn_editar = ctk.CTkButton(self.menu_lateral, text="Editar Cliente", fg_color="#005C99", command=self.preparar_edicion)
        self.btn_editar.pack(padx=20, pady=10)

        # 4. Área de Contenido Central
        self.area_principal = ctk.CTkFrame(self, corner_radius=10)
        self.area_principal.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Al arrancar, mostramos la tabla por defecto
        self.mostrar_tabla()

    # --- AQUÍ EMPIEZAN LAS FUNCIONES (Nota que están alineadas a la izquierda) ---

    def mostrar_tabla(self):
        # Limpiar el área central
        for widget in self.area_principal.winfo_children():
            widget.destroy()
        
        lbl = ctk.CTkLabel(self.area_principal, text="Listado de Clientes", font=ctk.CTkFont(size=18, weight="bold"))
        lbl.pack(pady=10)

        self.txt_output = ctk.CTkTextbox(self.area_principal, width=500, height=300)
        self.txt_output.pack(padx=20, pady=10, expand=True, fill="both")
        
        # Llamamos a la carga de datos
        self.cargar_datos()

    def mostrar_formulario(self):
        for widget in self.area_principal.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.area_principal, text="Nuevo Registro", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        self.ent_nombre = ctk.CTkEntry(self.area_principal, placeholder_text="Nombre Cliente", width=250)
        self.ent_nombre.pack(pady=5)
        
        self.ent_empresa = ctk.CTkEntry(self.area_principal, placeholder_text="Empresa", width=250)
        self.ent_empresa.pack(pady=5)

        btn_save = ctk.CTkButton(self.area_principal, text="Guardar Cliente", fg_color="green", command=self.validar_y_guardar)
        btn_save.pack(pady=20)

    def cargar_datos(self):
        self.txt_output.delete("1.0", "end")
        con = obtener_conexion()
        if con:
            cursor = con.cursor()
            # Ahora pedimos también el ID (la llave primaria)
            cursor.execute("SELECT id, nombre, empresa FROM clientes")
            for (id_cliente, nombre, empresa) in cursor:
                # Mostramos el ID para saber a quién borrar
                self.txt_output.insert("end", f"🆔 {id_cliente} | 👤 {nombre} | 🏢 {empresa}\n")
            con.close()
        else:
            self.txt_output.insert("end", "❌ No se pudo conectar.")

    def validar_y_guardar(self):
        # 1. Capturamos lo que escribiste en las cajas de texto (los Entries)
        nombre = self.ent_nombre.get()
        empresa = self.ent_empresa.get()

        # 2. Validación: No permitimos campos vacíos (como un "Required" en Access)
        if not nombre or not empresa:
            print("⚠️ Error: Debes completar Nombre y Empresa")
            # Podríamos mostrar un mensaje en la interfaz aquí después
            return

        # 3. Proceso de Guardado
        con = obtener_conexion()
        if con:
            try:
                cursor = con.cursor()
                # El comando SQL (usamos %s para evitar ataques de inyección SQL, es buena práctica)
                sql = "INSERT INTO clientes (nombre, empresa) VALUES (%s, %s)"
                valores = (nombre, empresa)
                
                cursor.execute(sql, valores)
                
                # ¡VITAL! Sin el commit, los datos no se escriben físicamente en el disco
                con.commit()
                
                print(f"✅ Cliente {nombre} guardado exitosamente.")
                
                # 4. Feedback al usuario: Volvemos a la tabla para ver el nuevo registro
                self.mostrar_tabla()
                
            except Exception as e:
                print(f"❌ Error al insertar: {e}")
            finally:
                con.close()
 
    def eliminar_cliente(self):
        # 1. Pedir el ID (Usaremos un cuadro de diálogo simple de CustomTkinter)
        dialogo = ctk.CTkInputDialog(text="Escribe el ID del cliente a borrar:", title="Borrar Registro")
        id_a_borrar = dialogo.get_input()

        if id_a_borrar:
            con = obtener_conexion()
            if con:
                try:
                    cursor = con.cursor()
                    # Aquí aplicamos la seguridad del %s
                    sql = "DELETE FROM clientes WHERE id = %s"
                    cursor.execute(sql, (id_a_borrar,)) # La coma es necesaria porque espera una lista
                    
                    con.commit()
                    print(f"🗑️ Registro {id_a_borrar} eliminado.")
                    self.mostrar_tabla() # Refrescamos la lista
                except Exception as e:
                    print(f"❌ Error al borrar: {e}")
                finally:
                    con.close()

    def preparar_edicion(self):
        # 1. Preguntamos qué ID queremos editar
        dialogo = ctk.CTkInputDialog(text="ID del cliente a editar:", title="Editar Registro")
        id_editar = dialogo.get_input()

        if id_editar:
            con = obtener_conexion()
            if con:
                cursor = con.cursor()
                # Traemos los datos actuales de ese ID específico
                cursor.execute("SELECT nombre, empresa FROM clientes WHERE id = %s", (id_editar,))
                resultado = cursor.fetchone() # Traemos solo una fila
                con.close()

                if resultado:
                    # Si el cliente existe, abrimos el formulario pero "relleno"
                    self.mostrar_formulario_edicion(id_editar, resultado[0], resultado[1])
                else:
                    print(f"❌ No se encontró el ID {id_editar}")

    def mostrar_formulario_edicion(self, id_cliente, nombre_actual, empresa_actual):
        # Limpiamos el área central
        for widget in self.area_principal.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.area_principal, text=f"Editando Cliente ID: {id_cliente}", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        # Cajas de texto con el valor actual ya puesto
        self.ent_nombre = ctk.CTkEntry(self.area_principal, width=250)
        self.ent_nombre.insert(0, nombre_actual) # Insertamos el nombre viejo
        self.ent_nombre.pack(pady=5)
        
        self.ent_empresa = ctk.CTkEntry(self.area_principal, width=250)
        self.ent_empresa.insert(0, empresa_actual) # Insertamos la empresa vieja
        self.ent_empresa.pack(pady=5)

        # Botón para GUARDAR CAMBIOS
        # Usamos una función "lambda" para pasarle el ID al botón
        btn_update = ctk.CTkButton(self.area_principal, text="Actualizar Datos", fg_color="blue", command=lambda: self.ejecutar_actualizacion(id_cliente))
        btn_update.pack(pady=20)

    def ejecutar_actualizacion(self, id_cliente):
        nuevo_nombre = self.ent_nombre.get()
        nueva_empresa = self.ent_empresa.get()

        con = obtener_conexion()
        if con:
            try:
                cursor = con.cursor()
                # El comando UPDATE: "Actualiza la tabla clientes poniendo estos valores donde el ID sea este"
                sql = "UPDATE clientes SET nombre = %s, empresa = %s WHERE id = %s"
                cursor.execute(sql, (nuevo_nombre, nueva_empresa, id_cliente))
                con.commit()
                
                print(f"✅ ID {id_cliente} actualizado correctamente.")
                self.mostrar_tabla() # Volvemos a la lista para ver el cambio
            except Exception as e:
                print(f"❌ Error al actualizar: {e}")
            finally:
                con.close()

if __name__ == "__main__":
    app = AppCRM()
    app.mainloop()