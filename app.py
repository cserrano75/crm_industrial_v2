import customtkinter as ctk
from database import obtener_conexion  # Importamos tu función de ayer


class AppCRM(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. Configuración de la Ventana
        self.title("Sistema de Gestión B2B - CRM")
        self.geometry("800x450")
        ctk.set_appearance_mode("light") # Estilo corporativo claro

        # 2. Diseño del Layout (Grid)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 3. Menú Lateral
        self.menu_lateral = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.menu_lateral.grid(row=0, column=0, sticky="nsew")
        
        self.lbl_logo = ctk.CTkLabel(self.menu_lateral, text="CRM DE GESTION", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_logo.pack(pady=20)

        self.btn_listar = ctk.CTkButton(self.menu_lateral, text="Listar Clientes", command=self.cargar_datos)
        self.btn_listar.pack(padx=20, pady=10)

        # 4. Área de Contenido
        self.area_principal = ctk.CTkFrame(self, corner_radius=10)
        self.area_principal.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.txt_output = ctk.CTkTextbox(self.area_principal, width=500, height=300)
        self.txt_output.pack(padx=10, pady=10, expand=True, fill="both")

    def cargar_datos(self):
        # Limpiamos el cuadro de texto
        self.txt_output.delete("1.0", "end")
        
        con = obtener_conexion()
        if con:
            cursor = con.cursor()
            cursor.execute("SELECT nombre, empresa FROM clientes")
            for (nombre, empresa) in cursor:
                self.txt_output.insert("end", f"👤 Cliente: {nombre} | 🏢 Empresa: {empresa}\n")
            con.close()
        else:
            self.txt_output.insert("end", "❌ No se pudo conectar a la base de datos.")

if __name__ == "__main__":
    
    app = AppCRM()
    app.mainloop()