import customtkinter as ctk
from crm_backend import GestorClientes  # <--- IMPORTAMOS AL EXPERTO
import os # Pon esto al principio del archivo
from tkinter import messagebox # <--- Herramienta de alertas estándar

class AppCRM(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ==========================================
        # 1. CONFIGURACIÓN ESTRUCTURAL (EL CHASIS)
        # ==========================================
        self.title("Sistema de Gestión B2B - CRM Industrial")
        self.geometry("900x600") # Aumenté un poco el ancho para comodidad
        ctk.set_appearance_mode("light")

        # Configuración de proporciones (Layout)
        self.grid_columnconfigure(1, weight=1) # El área derecha crece
        self.grid_rowconfigure(0, weight=1)    # Toda la altura disponible

        # ==========================================
        # 2. PANEL LATERAL (Navegación y Estados)
        # ==========================================
        self.menu_lateral = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.menu_lateral.grid(row=0, column=0, sticky="nsew")
        
        # Identificador del Sistema
        ctk.CTkLabel(self.menu_lateral, text="MENU CRM", 
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        # Indicadores Financieros (API en Tiempo Real)
        # Etiqueta Dólar (Color Negro para mejor lectura)
        self.label_dolar = ctk.CTkLabel(self.menu_lateral, text="Dólar: Cargando...", 
                                        font=("Arial", 12, "bold"), text_color="black")
        self.label_dolar.pack(padx=20, pady=(0, 2))

        # Etiqueta UF (Color Negro)
        self.label_uf = ctk.CTkLabel(self.menu_lateral, text="UF: Cargando...", 
                                     font=("Arial", 12, "bold"), text_color="black")
        self.label_uf.pack(padx=20, pady=(0, 20))

        # --- SECCIÓN DE BOTONES (ACCIONES) ---
        # Botón para abrir la Calculadora
        self.btn_calc = ctk.CTkButton(self.menu_lateral, text="🧮 Calculadora Express", 
                                      fg_color="#34495E", # Un gris azulado sobrio
                                      command=self.abrir_calculadora)
        self.btn_calc.pack(padx=20, pady=10)

        # Listado y Búsqueda
        ctk.CTkButton(self.menu_lateral, text="Listar Clientes", 
                      command=self.mostrar_tabla).pack(padx=20, pady=10)
        
        # Operaciones CRUD (Crear, Editar, Borrar)
        ctk.CTkButton(self.menu_lateral, text="Nuevo Registro", 
                      command=self.mostrar_formulario).pack(padx=20, pady=10)
        ctk.CTkButton(self.menu_lateral, text="Editar Cliente", 
                      command=self.preparar_edicion).pack(padx=20, pady=10)
        ctk.CTkButton(self.menu_lateral, text="Borrar Cliente", fg_color="#A30000", 
                      command=self.eliminar_cliente).pack(padx=20, pady=10)

        # Herramientas de Reportabilidad y Datos
        self.btn_pdf = ctk.CTkButton(self.menu_lateral, text="Generar PDF", 
                                     fg_color="#5D3FD3", command=self.generar_reporte)
        self.btn_pdf.pack(padx=20, pady=10)

        self.btn_importar = ctk.CTkButton(self.menu_lateral, text="Importar Excel", 
                                          fg_color="#228B22", command=self.ejecutar_importacion)
        self.btn_importar.pack(padx=20, pady=10)

        # Cierre de Sesión (Al pie del menú)
        self.espaciador = ctk.CTkLabel(self.menu_lateral, text="")
        self.espaciador.pack(expand=True, fill="both") 

        self.btn_salir = ctk.CTkButton(self.menu_lateral, text="Cerrar Sistema", 
                                       fg_color="#A30000", hover_color="#7A0000", 
                                       command=self.salir_app)
        self.btn_salir.pack(padx=20, pady=20, side="bottom")

        # ==========================================
        # 3. ÁREA DE TRABAJO (CONTENIDO DINÁMICO)
        # ==========================================
        self.area_principal = ctk.CTkFrame(self, corner_radius=10)
        self.area_principal.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Cabecera del área de trabajo
        ctk.CTkLabel(self.area_principal, text="Gestión de Clientes", 
                     font=("Arial", 22, "bold")).pack(pady=10)

        # Componente de Búsqueda (Fijo en la parte superior)
        self.entry_busqueda = ctk.CTkEntry(self.area_principal, 
                                           placeholder_text="🔍 Buscar por nombre o empresa...", width=450)
        self.entry_busqueda.pack(pady=5)
        self.entry_busqueda.bind("<KeyRelease>", self.ejecutar_busqueda)

        # Visor de Datos (Widget Multilínea)
        self.txt_output = ctk.CTkTextbox(self.area_principal, width=550, height=350)
        self.txt_output.pack(padx=20, pady=10, expand=True, fill="both")

        # ==========================================
        # 4. INICIALIZACIÓN DE DATOS
        # ==========================================
        self.mostrar_tabla()           # Carga inicial de la BD
        self.actualizar_indicadores()  # Carga inicial del Dólar

    # --- FUNCIONES DE NAVEGACIÓN (INTERFAZ) ---

    def mostrar_tabla(self, filtro=""):
        # Solo limpiamos el área de resultados, no el buscador si está afuera
        self.txt_output.delete("1.0", "end") 

        # Pedimos los datos al Gestor
        clientes = GestorClientes.listar(filtro) 
        
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
        # 1. Capturamos y "limpiamos" los datos (Quita espacios extras)
        n = self.ent_nombre.get().strip()
        e = self.ent_empresa.get().strip()

        # 2. AUDITORÍA: Si cualquiera de los dos está vacío...
        if not n or not e:
            messagebox.showwarning("Faltan Datos", "Por favor, completa Nombre y Empresa.")
            return # Detiene la ejecución aquí mismo

        # 3. EJECUCIÓN: Si pasó la auditoría, llamamos al Backend
        if GestorClientes.guardar(n, e):
            # 4. FEEDBACK: Avisamos al usuario que todo salió bien
            messagebox.showinfo("Éxito", f"Cliente {n} guardado correctamente.")
            
            # 5. LIMPIEZA: Dejamos el formulario listo para el próximo cliente
            self.ent_nombre.delete(0, 'end')
            self.ent_empresa.delete(0, 'end')
            
            # 6. ACTUALIZACIÓN: Refrescamos la vista de la tabla
            self.mostrar_tabla()
        else:
            # Si el GestorClientes.guardar falló (ej: se cayó la DB)
            messagebox.showerror("Error", "No se pudo guardar en la Base de Datos.")

    def ejecutar_busqueda(self, event=None):
        termino = self.entry_busqueda.get()
        # Llamamos a mostrar_tabla pero pasándole el filtro
        self.mostrar_tabla(filtro=termino)

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
        # Llamamos al backend para obtener ambos valores
        valor_dolar, valor_uf = GestorClientes.obtener_indicadores()
        
        if valor_dolar > 0 and valor_uf > 0:
            # Formateamos con separador de miles para Chile
            self.label_dolar.configure(text=f"Dólar: ${valor_dolar:,.2f}")
            self.label_uf.configure(text=f"UF: ${valor_uf:,.2f}")
        else:
            self.label_dolar.configure(text="Dólar: Sin conexión")
            self.label_uf.configure(text="UF: Sin conexión")
        
    def abrir_calculadora(self):
        ventana_calc = ctk.CTkToplevel(self)
        ventana_calc.title("Calculadora de Cotización con Registro")
        ventana_calc.geometry("450x450")
        ventana_calc.after(100, lambda: ventana_calc.focus_force())

        # --- LÓGICA DE DATOS ---
        try:
            # 1. Obtenemos indicadores actuales
            dolar_actual = float(self.label_dolar.cget("text").split('$')[1].replace(',', ''))
            uf_actual = float(self.label_uf.cget("text").split('$')[1].replace(',', ''))
            
            # 2. Traemos la lista de clientes para el selector
            lista_clientes = GestorClientes.listar() # Trae [id, nombre, empresa]
            # Formateamos para que se vea: "ID - Nombre (Empresa)"
            opciones_clientes = [f"{c[0]} - {c[1]} ({c[2]})" for c in lista_clientes]
        except Exception as e:
            messagebox.showerror("Error", f"Faltan datos base: {e}")
            ventana_calc.destroy()
            return

        # --- INTERFAZ DE LA CALCULADORA ---
        ctk.CTkLabel(ventana_calc, text="1. Seleccione Cliente:", font=("Arial", 12, "bold")).pack(pady=(15, 0))
        
        # Selector de Clientes (Combobox)
        combo_clientes = ctk.CTkComboBox(ventana_calc, values=opciones_clientes, width=350)
        combo_clientes.pack(pady=5)

        ctk.CTkLabel(ventana_calc, text="2. Monto a Cotizar (USD o UF):", font=("Arial", 12, "bold")).pack(pady=(15, 0))
        ent_monto = ctk.CTkEntry(ventana_calc, placeholder_text="Ej: 1500.50", width=200)
        ent_monto.pack(pady=5)

        lbl_resultado = ctk.CTkLabel(ventana_calc, text="Resultados aparecerán aquí", font=("Arial", 11))
        lbl_resultado.pack(pady=20)

        # --- FUNCIÓN INTERNA DE CÁLCULO Y REGISTRO ---
        def procesar_y_guardar():
            try:
                # Captura de datos
                monto = float(ent_monto.get().replace(',', '.'))
                seleccion = combo_clientes.get()
                id_cliente = int(seleccion.split(" - ")[0]) # Extraemos el ID
                
                # Cálculos
                res_dolar = monto * dolar_actual
                res_uf = monto * uf_actual
                
                # Actualizamos la etiqueta visual
                lbl_resultado.configure(text=f"💵 USD a CLP: ${res_dolar:,.0f}\n🏗️ UF a CLP: ${res_uf:,.0f}", text_color="blue")

                # GUARDADO EN BD (Aquí usamos tu función registrar_cotizacion)
                # Guardamos por defecto el cálculo en UF como total (puedes ajustarlo)
                GestorClientes.registrar_cotizacion(id_cliente, monto, dolar_actual, uf_actual, res_uf)
                
                messagebox.showinfo("Éxito", "Cotización registrada en el historial del cliente.")
            except ValueError:
                messagebox.showwarning("Atención", "Por favor, ingrese un monto numérico válido.")
            except Exception as e:
                messagebox.showerror("Error de BD", f"No se pudo guardar: {e}")

        # Botón Maestro
        ctk.CTkButton(ventana_calc, text="Calcular y Registrar", 
                      fg_color="#27AE60", command=procesar_y_guardar).pack(pady=10)

        def calcular():
            try:
                monto = float(ent_monto.get().replace(',', '.'))
                res_dolar = monto * dolar_actual
                res_uf = monto * uf_actual
                
                texto = (f"Monto ingresado: {monto:,.2f}\n\n"
                         f"💵 En Pesos (Dólar): ${res_dolar:,.0f} CLP\n"
                         f"🏗️ En Pesos (UF): ${res_uf:,.0f} CLP")
                
                lbl_resultado.configure(text=texto, text_color="black")
            except:
                messagebox.showwarning("Error", "Ingrese un número válido.")

        # Botón de cálculo dentro de la ventana
        ctk.CTkButton(ventana_calc, text="Convertir a CLP", command=calcular).pack(pady=10)

if __name__ == "__main__":
    app = AppCRM()
    app.mainloop()