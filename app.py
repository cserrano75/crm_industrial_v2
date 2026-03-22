import customtkinter as ctk
from crm_backend import GestorClientes  # <--- IMPORTAMOS AL EXPERTO
import os # Pon esto al principio del archivo

class AppCRM(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. Configuración de la Ventana
        self.title("Sistema de Gestión B2B - CRM Industrial")
        self.geometry("800x500")
        ctk.set_appearance_mode("light")

        # 2. Diseño del Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 3. Menú Lateral
        self.menu_lateral = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.menu_lateral.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.menu_lateral, text="MENU CRM", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        # NUEVO: Etiqueta del Dólar
        self.label_dolar = ctk.CTkLabel(self.menu_lateral, 
                                        text="Cargando dólar...", 
                                        font=("Arial", 12, "italic"),
                                        text_color="#F1C40F") # Un amarillo suave para que resalte
        self.label_dolar.pack(padx=20, pady=5)

        # BOTONES: Todos llaman a funciones de la Interfaz
        ctk.CTkButton(self.menu_lateral, text="Listar Clientes", command=self.mostrar_tabla).pack(padx=20, pady=10)
        ctk.CTkButton(self.menu_lateral, text="Nuevo Registro", command=self.mostrar_formulario).pack(padx=20, pady=10)
        ctk.CTkButton(self.menu_lateral, text="Editar Cliente", command=self.preparar_edicion).pack(padx=20, pady=10)
        ctk.CTkButton(self.menu_lateral, text="Borrar Cliente", fg_color="#A30000", command=self.eliminar_cliente).pack(padx=20, pady=10)

        # Antes decía command=self.descargar_pdf
        self.btn_pdf = ctk.CTkButton(self.menu_lateral, text="Generar PDF", 
                             fg_color="#5D3FD3", 
                             command=self.generar_reporte) # <--- Nombre normalizado
        self.btn_pdf.pack(padx=20, pady=10)

        # Boton Importar Excel
        self.btn_importar = ctk.CTkButton(self.menu_lateral, text="Importar Excel", 
                                          fg_color="#228B22", # Verde bosque profesional
                                          command=self.ejecutar_importacion)
        self.btn_importar.pack(padx=20, pady=10)

        # 1. Agregamos un Label vacío que "empuja" todo hacia abajo
        self.espaciador = ctk.CTkLabel(self.menu_lateral, text="")
        self.espaciador.pack(expand=True, fill="both") 

        # 2. El botón de salida técnica
        self.btn_salir = ctk.CTkButton(self.menu_lateral, 
                                      text="Cerrar Sistema", 
                                      fg_color="#A30000",      # Rojo oscuro (Alerta)
                                      hover_color="#7A0000",   # Rojo más profundo al pasar el mouse
                                      command=self.salir_app)
        self.btn_salir.pack(padx=20, pady=20, side="bottom")

        # 4. Área de Contenido Central
        self.area_principal = ctk.CTkFrame(self, corner_radius=10)
        self.area_principal.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.mostrar_tabla() # Arrancamos viendo la tabla
        self.actualizar_indicadores()

    # --- FUNCIONES DE NAVEGACIÓN (INTERFAZ) ---

    def mostrar_tabla(self):
        self.limpiar_pantalla()
        ctk.CTkLabel(self.area_principal, text="Listado de Clientes", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        self.txt_output = ctk.CTkTextbox(self.area_principal, width=500, height=300)
        self.txt_output.pack(padx=20, pady=10, expand=True, fill="both")
        
        # [LOGICA]: Pedimos los datos al Gestor
        clientes = GestorClientes.listar()
        for (id_c, nombre, empresa) in clientes:
            self.txt_output.insert("end", f"🆔 {id_c} | 👤 {nombre} | 🏢 {empresa}\n")

    def mostrar_formulario(self):
        self.limpiar_pantalla()
        ctk.CTkLabel(self.area_principal, text="Nuevo Registro", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        self.ent_nombre = ctk.CTkEntry(self.area_principal, placeholder_text="Nombre Cliente", width=250)
        self.ent_nombre.pack(pady=5)
        self.ent_empresa = ctk.CTkEntry(self.area_principal, placeholder_text="Empresa", width=250)
        self.ent_empresa.pack(pady=5)

        ctk.CTkButton(self.area_principal, text="Guardar Cliente", fg_color="green", command=self.validar_y_guardar).pack(pady=20)

    # --- FUNCIONES DE ACCIÓN (PUENTE ENTRE INTERFAZ Y LOGICA) ---

    def validar_y_guardar(self):
        n = self.ent_nombre.get()
        e = self.ent_empresa.get()
        if n and e:
            # [LOGICA]: El Gestor hace el INSERT
            if GestorClientes.guardar(n, e):
                self.mostrar_tabla()
        else:
            print("Faltan datos")

    def eliminar_cliente(self):
        dialogo = ctk.CTkInputDialog(text="ID a borrar:", title="Borrar")
        id_b = dialogo.get_input()
        if id_b and GestorClientes.borrar(id_b): # [LOGICA]: El Gestor hace el DELETE
            self.mostrar_tabla()

    def preparar_edicion(self):
        dialogo = ctk.CTkInputDialog(text="ID a editar:", title="Editar")
        id_e = dialogo.get_input()
        if id_e:
            # [LOGICA]: Pedimos al gestor un cliente específico (Necesitaremos crear esta función en backend)
            cliente = GestorClientes.obtener_uno(id_e)
            if cliente:
                self.mostrar_formulario_edicion(id_e, cliente[0], cliente[1])

    def mostrar_formulario_edicion(self, id_c, nombre, empresa):
        self.limpiar_pantalla()
        self.ent_nombre = ctk.CTkEntry(self.area_principal, width=250)
        self.ent_nombre.insert(0, nombre)
        self.ent_nombre.pack(pady=5)
        
        self.ent_empresa = ctk.CTkEntry(self.area_principal, width=250)
        self.ent_empresa.insert(0, empresa)
        self.ent_empresa.pack(pady=5)

        ctk.CTkButton(self.area_principal, text="Actualizar", command=lambda: self.finalizar_edicion(id_c)).pack(pady=20)

    def finalizar_edicion(self, id_c):
        n = self.ent_nombre.get()
        e = self.ent_empresa.get()
        # [LOGICA]: El Gestor hace el UPDATE (Necesitaremos crear esta función en backend)
        if GestorClientes.actualizar(id_c, n, e):
            self.mostrar_tabla()

    def limpiar_pantalla(self):
        for widget in self.area_principal.winfo_children():
            widget.destroy()

    # Antes decía def descargar_pdf(self):
    def generar_reporte(self): # <--- Ahora coincide con el comando del botón
        # 1. Desactivamos el botón para evitar clics dobles
        self.btn_pdf.configure(state="disabled", text="Generando...")
        if GestorClientes.generar_reporte_pdf():
            print("📁 Reporte generado.")
            # ESTO ABRE EL ARCHIVO AUTOMÁTICAMENTE:
            os.startfile("Reporte_Clientes.pdf") 
        else:
            print("❌ Error")
            
        # 3. Lo reactivamos al terminar
        self.btn_pdf.configure(state="normal", text="Generar PDF")

    def ejecutar_importacion(self):
        # Llamamos al experto (Backend)
        if GestorClientes.importar_desde_excel():
            print("✅ Datos importados con éxito.")
            self.mostrar_tabla() # Refrescamos la vista para ver los nuevos clientes
        else:
            print("❌ No se pudo importar el archivo. Verifica que se llame 'clientes.xlsx'")

    def salir_app(self):
        print("⚙️ Cerrando procesos y base de datos...")
        self.destroy() # Cierra la ventana de forma elegante

    def actualizar_indicadores(self):
        # Le pedimos al experto (Backend) que traiga el dato
        info_dolar = GestorClientes.obtener_dolar_dia()
        self.label_dolar.configure(text=info_dolar)
        
if __name__ == "__main__":
    app = AppCRM()
    app.mainloop()