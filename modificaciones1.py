import tkinter as tk
from tkinter import PhotoImage, messagebox
from PIL import Image, ImageTk
import datetime
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial
import pandas as pd
import os
import matplotlib.pyplot as plt

class JYDHI(tk.Tk): # JYDHI
    def __init__(self):
        super().__init__()
        self.title("JYDHI INICIO")
        self.state("zoomed")
        self.iconbitmap('JYDHI_LOGO.ico')

        self.ventana_principal = tk.Frame(self, bg="white")
        self.ventana_principal.grid(padx=0, pady=0, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.ventanas = {}

        for V in (Ventana_1, Ventana_crear_contraseña, Ventana_recuperar_contraseña, Ventana_2, Ventana_3):
            ventana = V(self.ventana_principal, self)  
            self.ventanas[V] = ventana
            ventana.grid(row=0, column=0, sticky="nsew") 
        self.mostrar_ventana(Ventana_1) 
    
    def mostrar_ventana(self, ventana_clase):
        ventana = self.ventanas[ventana_clase]
        ventana.tkraise()

        if ventana_clase == Ventana_1:
            ventana.limpiar_campos()

class Ventana_1(tk.Frame):  # INICIO DE SESIÓN
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="white", width=1365, height=767)

        # Logo
        self.logo = PhotoImage(file="JYDHI_INICIO.png")
        tk.Label(self, image=self.logo, bg='white').place(x=120, y=300)

        # Marco para información de inicio de sesión
        self.marco_informacion = tk.Frame(self, width=450, height=500, bg='white')
        self.marco_informacion.place(x=720, y=140)

        # Título de bienvenida
        self.titulo_bienvenida = tk.Label(self.marco_informacion, text='BIENVENIDO A JYDHI', fg='#BE2623', bg='white', font=('Arial', 28))
        self.titulo_bienvenida.place(x=30, y=5)

        # Entrada de usuario
        self.usuario = tk.Entry(self.marco_informacion, width=25, fg='#0E3746', border=0, bg='white', font=('Arial', 16))
        self.usuario.place(x=30, y=100)
        self.usuario.insert(0, 'Usuario')
        self.usuario.bind('<FocusIn>', self.entrada_usuario)
        self.usuario.bind('<FocusOut>', self.dejar_usuario)
        tk.Frame(self.marco_informacion, width=400, height=1, bg='#0E3746').place(x=30, y=135)

        # Entrada de contraseña (ocultar caracteres con '*')
        self.contraseña = tk.Entry(self.marco_informacion, width=25, fg='#0E3746', border=0, bg='white', font=('Arial', 16))
        self.contraseña.place(x=30, y=210)
        self.contraseña.insert(0, 'Contraseña')
        self.contraseña.bind('<FocusIn>', self.entrada_contraseña)
        self.contraseña.bind('<FocusOut>', self.dejar_contraseña)
        tk.Frame(self.marco_informacion, width=400, height=1, bg='#0E3746').place(x=30, y=245)

        # Botón para iniciar sesión
        tk.Button(self.marco_informacion, width=40, pady=7, text='Iniciar sesión', font=('Arial'), bg='#BE2623', fg='#F4F2EC', border=0, command=self.iniciar_sesion).place(x=45, y=310)

        # Etiqueta de cuenta
        etiqueta_sin_cuenta = tk.Label(self.marco_informacion, text='¿Aún no tienes una cuenta?', fg='#0E3746', bg='white', font=('Arial', 12))
        etiqueta_sin_cuenta.place(x=70, y=380)

        # Botón de crear cuenta
        tk.Button(self.marco_informacion, width=12, text='Crear cuenta', font=('Arial', 12), border=0, bg='white', cursor='hand2', fg='#BE2623', command=self.crear_cuenta).place(x=270, y=378)

        # Botón de olvidé mis credenciales
        tk.Button(self.marco_informacion, width=40, text='Olvidé mis credenciales', font=('Arial', 12), border=0, bg='white', cursor='hand2', fg='#17617B', command=self.recuperar_cuenta).place(x=45, y=265)

        # Para presionar enter para iniciar sesión 
        self.usuario.bind('<Return>', lambda event: self.iniciar_sesion())  
        self.contraseña.bind('<Return>', lambda event: self.iniciar_sesion()) 

    def entrada_usuario(self, e):
        self.usuario.delete(0, 'end')

    def dejar_usuario(self, e):
        if not self.usuario.get():
            self.usuario.insert(0, 'Usuario')

    def entrada_contraseña(self, e):
        self.contraseña.delete(0, 'end')
        self.contraseña.config(show='*')

    def dejar_contraseña(self, e):
        if not self.contraseña.get():
            self.contraseña.insert(0, 'Contraseña')

    def limpiar_campos(self):
        self.usuario.delete(0, 'end')
        self.usuario.insert(0, 'Usuario')
        self.contraseña.delete(0, 'end')
        self.contraseña.config(show='')
        self.contraseña.insert(0, 'Contraseña')

    def iniciar_sesion(self):
        usuario = self.usuario.get()
        contraseña = self.contraseña.get()
        usuarios = {"a": {"Contraseña": "1"}}

        if usuario in usuarios and usuarios[usuario]["Contraseña"] == contraseña:
            self.controller.mostrar_ventana(Ventana_2)
        else:
            messagebox.showerror("INCORRECTO", "Credenciales incorrectas")
    
    def crear_cuenta(self):
        self.controller.mostrar_ventana(Ventana_crear_contraseña)

    def recuperar_cuenta(self):
        self.controller.mostrar_ventana(Ventana_recuperar_contraseña)

class Ventana_crear_contraseña(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="white")

        contenido_frame = tk.Frame(self, bg="#F5F4F2", highlightbackground="#E0E0E0", highlightthickness=2)
        contenido_frame.place(relx=0.5, rely=0.5, anchor="center", width=1100, height=540)

        # Logo y título
        logo_img = tk.PhotoImage(file="imagen_REcontra.png")  # Imagen del logo
        logo_resized = logo_img.subsample(2, 2)  # por si les sirve esto reduce tamaño del logo
        tk.Label(contenido_frame, image=logo_resized, bg="#F5F4F2").place(x=20, y=15)
        self.logo_resized = logo_resized 

        tk.Label(contenido_frame, text="JYDHI", font=("Arial", 24, "bold"), bg="#F5F4F2", fg="#0A3F44").place(x=70, y=20)
        tk.Label(contenido_frame, text="CREAR CUENTA", font=("Arial", 20), bg="#F5F4F2", fg="#0A3F44").place(x=190, y=25)

        # Icono de perfil
        perfil_img = Image.open("Imagen_usuario.png")  
        perfil_resized = perfil_img.resize((190, 190))  # ajusta las dimensiones (Pillow)
        perfil_resized = ImageTk.PhotoImage(perfil_resized)
        tk.Label(contenido_frame, image=perfil_resized, bg="#F5F4F2").place(x=70, y=100)
        self.perfil_img = perfil_resized 

        # Para daots de entrada
        tk.Label(contenido_frame, text="Nombre:", font=("Arial", 14), bg="#F5F4F2", fg="#0A3F44").place(x=300, y=130)
        tk.Entry(contenido_frame, font=("Arial", 12), width=50).place(x=380, y=131)

        tk.Label(contenido_frame, text="Turno:", font=("Arial", 14), bg="#F5F4F2", fg="#0A3F44").place(x=300, y=190)
        tk.Entry(contenido_frame, font=("Arial", 12), width=52).place(x=361, y=191)

        tk.Label(contenido_frame, text="Ingrese clave para el registro:", font=("Arial", 14), bg="#F5F4F2", fg="#0A3F44").place(x=300, y=250)
        tk.Entry(contenido_frame, font=("Arial", 12), width=30, show="*").place(x=558, y=251)

        # para usuario y contraseña
        tk.Label(contenido_frame, text="Usuario:", font=("Arial", 14), bg="#F5F4F2", fg="red").place(x=150, y=350)
        tk.Entry(contenido_frame, font=("Arial", 12), width=45).place(x=225, y=351)

        tk.Label(contenido_frame, text="Ingrese una contraseña:", font=("Arial", 14), bg="#F5F4F2", fg="red").place(x=150, y=400)
        tk.Entry(contenido_frame, font=("Arial", 12), width=30, show="*").place(x=359, y=401)

        # Botones 
        tk.Button(contenido_frame, text="Verificar clave", font=("Arial", 12), bg="#0A3F44", fg="white", command=self.verificar_clave).place(x=837, y=246)
        tk.Button(contenido_frame, text="Crear cuenta", font=("Arial", 12), bg="#0A3F44", fg="white", command=self.crear_cuenta).place(x=640, y=396)

        # Botón para regresar a Iniciar sesión
        tk.Button(
            contenido_frame,
            text="Regresar a Iniciar sesión",
            font=("Arial", 12),
            bg='#BE2623', fg='#F4F2EC', border=0,
            command=lambda: self.controller.mostrar_ventana(Ventana_1)
        ).place(x=50, y=500)

    def verificar_clave(self):
        print("Verificando clave...")

    def crear_cuenta(self):
        print("Creando cuenta...")

class Ventana_recuperar_contraseña(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="white")

        contenido_frame = tk.Frame(self, bg="#F5F4F2", highlightbackground="#E0E0E0", highlightthickness=2)
        contenido_frame.place(relx=0.5, rely=0.5, anchor="center", width=1100, height=540)

        # Logo y título
        logo_img = tk.PhotoImage(file="imagen_REcontra.png")  
        logo_resized = logo_img.subsample(2, 2)  # por si les sirve esto reduce tamaño del logo
        tk.Label(contenido_frame, image=logo_resized, bg="#F5F4F2").place(x=20, y=15)
        self.logo_resized = logo_resized  

        tk.Label(contenido_frame, text="JYDHI", font=("Arial", 24, "bold"), bg="#F5F4F2", fg="#0A3F44").place(x=70, y=20)
        tk.Label(contenido_frame, text="RECUPERAR CUENTA", font=("Arial", 20), bg="#F5F4F2", fg="#0A3F44").place(x=190, y=25)

        # Icono de perfil
        perfil_img = Image.open("Imagen_usuario.png")
        perfil_resized = perfil_img.resize((190, 190))  # ajusta las dimensiones
        perfil_resized = ImageTk.PhotoImage(perfil_resized)
        tk.Label(contenido_frame, image=perfil_resized, bg="#F5F4F2").place(x=70, y=100)
        self.perfil_img = perfil_resized

        # Datos de entrada
        tk.Label(contenido_frame, text="Nombre:", font=("Arial", 14), bg="#F5F4F2", fg="#0A3F44").place(x=300, y=100)
        tk.Entry(contenido_frame, font=("Arial", 12), width=51).place(x=381, y=101)

        tk.Label(contenido_frame, text="Turno:", font=("Arial", 14), bg="#F5F4F2", fg="#0A3F44").place(x=300, y=150)
        tk.Entry(contenido_frame, font=("Arial", 12), width=53).place(x=361, y=151)

        tk.Label(contenido_frame, text="Usuario:", font=("Arial", 14), bg="#F5F4F2", fg="#0A3F44").place(x=300, y=200)
        tk.Entry(contenido_frame, font=("Arial", 12), width=51, show="*").place(x=379, y=201)

        tk.Label(contenido_frame, text="Ingrese clave de recuperación:", font=("Arial", 14), bg="#F5F4F2", fg="#0A3F44").place(x=300, y=250)
        tk.Entry(contenido_frame, font=("Arial", 12), width=30, show="*").place(x=568, y=251)

        # Para usuario y contraseña
        tk.Label(contenido_frame, text="Usuario:", font=("Arial", 14), bg="#F5F4F2", fg="red").place(x=300, y=350)
        #tk.Entry(contenido_frame, font=("Arial", 12), width=30).place(x=374, y=351)

        tk.Label(contenido_frame, text="Contraseña:", font=("Arial", 14), bg="#F5F4F2", fg="red").place(x=300, y=400)
        #tk.Entry(contenido_frame, font=("Arial", 12), width=30, show="*").place(x=507, y=401)

        # Boton
        tk.Button(contenido_frame, text="Verificar clave", font=("Arial", 12), bg="#0A3F44", fg="white", command=self.verificar_clave).place(x=870, y=247)

        # Botón para regresar a Iniciar sesión
        tk.Button(
            contenido_frame,
            text="Regresar a Iniciar sesión",
            font=("Arial", 12),
            bg='#BE2623', fg='#F4F2EC', border=0,
            command=lambda: self.controller.mostrar_ventana(Ventana_1)
        ).place(x=50, y=500)

    def verificar_clave(self):
        print("Verificando clave...")

class Ventana_2(tk.Frame): # MENÚ PRINCIPAL 
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="#EAE8DC")
        
        # Frames :)
        self.marco_menu = tk.Frame(self, width=221, height=767, bg='white')  
        self.marco_menu.place(x=0, y=0)

        # Imagenes
        self.logo = PhotoImage(file='inicio_logo.png')
        tk.Label(self, image=self.logo, bg='white').place(x=50, y=80)
        self.logo2 = PhotoImage(file='inicio_usuario_rojo.png')
        tk.Label(self, image=self.logo2, bg='#EAE8DC').place(x=260, y=100)
        self.logo3 = PhotoImage(file='fondo_inicio.png')
        tk.Label(self, image=self.logo3, bg='#EAE8DC').place(x=221, y=175)


        # Titulos
        self.titulo_inicio = tk.Label(self, text='INICIO', fg='#BE2623', bg='#EAE8DC', font=('Arial', 24))
        self.titulo_inicio.place(x=280, y=40)
        self.titulo_usuario = tk.Label(self, text='HOLA ITZEL', fg='#BE2623', bg='#EAE8DC', font=('Arial', 20))
        self.titulo_usuario.place(x=370, y=125)
        self.hora_fecha = tk.Label(self, text='Fecha y hora: ', fg='#0E3746', bg='#EAE8DC', font=('Arial', 18))
        self.hora_fecha.place(x=800, y=130)
        self.nombre = tk.Label(self, text="Nombre: Itzel Adriana López Cárdenas", fg='#0E3746', bg='#EAE8DC', font=('Arial', 18))
        self.nombre.place(x=280, y=210)

        # Reloj
        self.hora_fecha = tk.Label(self, fg='#0E3746', bg='#EAE8DC', font=('Arial', 18))
        self.hora_fecha.place(x=960, y=130)
        self.actualizar_reloj()

        # Botones
        self.imagen_icono = PhotoImage(file='inicio_boton.png')
        self.boton = tk.Button(self.marco_menu, width=221, height=80, text="       Inicio", image=self.imagen_icono,  compound="left", font=("Arial", 14), fg="#0E3746", bg="#EAE8DC", border=0, command=lambda: controller.mostrar_ventana(Ventana_2))
        self.boton.place(x=0, y=300)
        self.imagen_icono2 = PhotoImage(file='inicio_registros.png')
        self.boton2 = tk.Button(self.marco_menu, width=221, height=80, text="    Registro", image=self.imagen_icono2,  compound="left", font=("Arial", 14), fg="#0E3746", bg="white", border=0, command=lambda: controller.mostrar_ventana(Ventana_3))
        self.boton2.place(x=0, y=400)
        tk.Button(self.marco_menu, width=18, pady=7, text='Cerrar sesión', font=('Arial'), bg='#BE2623', fg='white', border=0, activebackground='#EAE8DC' ,command=lambda: controller.mostrar_ventana(Ventana_1)).place(x=25, y=600)

    def actualizar_reloj(self):
        hora_actual = datetime.datetime.now().strftime('%d-%m-%Y  /  %H:%M:%S')
        self.hora_fecha.config(text=hora_actual)
        self.after(1000, self.actualizar_reloj)

class Ventana_3(tk.Frame): # RESGISTROS
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="#EAE8DC")

        # Frames :)
        self.marco_menu = tk.Frame(self, width=221, height=767, bg='white')  
        self.marco_menu.place(x=0, y=0)
        
        self.marco = tk.Frame(self, width=1020, height=70, bg='#17617B')
        self.marco.place(x=280, y=100)
        self.marco2 = tk.Frame(self, width=1020, height=420, bg='white')
        self.marco2.place(x=280, y=190)

        # Imagenes
        self.logo = PhotoImage(file='inicio_logo.png')
        tk.Label(self, image=self.logo, bg='white').place(x=50, y=80)
        self.logo2 = PhotoImage(file='ii.png')
        tk.Label(self.marco2, image=self.logo2, bg='white').place(x=35, y=90)

        # Titulos
        self.titulo_inicio = tk.Label(self, text='REGISTROS  |  Bienvenido al apartado de registros', fg='#BE2623', bg='#EAE8DC', font=('Arial', 24))
        self.titulo_inicio.place(x=280, y=40)
        self.indicaciones1 = tk.Label(self.marco, text='1. Seleccione la opción que desea realizar.', fg='white', bg='#17617B', font=('Arial', 14))
        self.indicaciones1.place(x=10, y=5)
        self.indicaciones2 = tk.Label(self.marco, text='2. Llene los campos con la información solicitada.', fg='white', bg='#17617B', font=('Arial', 14))
        self.indicaciones2.place(x=10, y=30)

        # Creación de dataframe :(
        self.pacientes = "ARCHIVOS DE PACIENTES"
        if not os.path.exists(self.pacientes):
            os.makedirs(self.pacientes)

        # Guardar los datos de las entradas :)
        self.nombre_del_paciente = tk.StringVar()
        self.fecha_de_nacimiento = tk.StringVar()
        self.usuario_del_paciente = tk.StringVar()
        self.edad_del_paciente = tk.StringVar()
        self.sexo_del_paciente = tk.StringVar()

        # Campos
        self.nombre = tk.Label(self.marco2, text='Nombre del paciente:', fg='#0E3746', bg='white', font=('Arial', 14))
        self.nombre.place(x=35, y=148)
        self.nombre_ = tk.Entry(self.marco2, width=68, fg='#0E3746', border=1, bg='white', font=('Arial', 14), state='disabled', textvariable=self.nombre_del_paciente)
        self.nombre_.place(x=228, y=148)

        self.fecha_nacimiento = tk.Label(self.marco2, text='Fecha de nacimiento:', fg='#0E3746', bg='white', font=('Arial', 14))
        self.fecha_nacimiento.place(x=35, y=178)
        self.fecha_ = tk.Entry(self.marco2, width=68, fg='#0E3746', border=1, bg='white', font=('Arial', 14), state='disabled', textvariable=self.fecha_de_nacimiento)
        self.fecha_.place(x=228, y=178)

        self.usuario = tk.Label(self.marco2, text='Usuario del paciente:', fg='#0E3746', bg='white', font=('Arial', 14))
        self.usuario.place(x=35, y=208)

        self.usuario_ = tk.Entry(self.marco2, width=68, fg='#0E3746', border=1, bg='white', font=('Arial', 14), state='disabled', textvariable=self.usuario_del_paciente)
        self.usuario_.place(x=228, y=208)

        self.edad = tk.Label(self.marco2, text='Edad:', fg='#0E3746', bg='white', font=('Arial', 14))
        self.edad.place(x=35, y=238)
        self.edad_ = tk.Entry(self.marco2, width=80, fg='#0E3746', border=1, bg='white', font=('Arial', 14), state='disabled', textvariable=self.edad_del_paciente)
        self.edad_.place(x=95, y=238)

        self.sexo = tk.Label(self.marco2, text='Sexo:', fg='#0E3746', bg='white', font=('Arial', 14))
        self.sexo.place(x=35, y=268)
        self.sexo_ = tk.Entry(self.marco2, width=80, fg='#0E3746', border=1, bg='white', font=('Arial', 14), state='disabled', textvariable=self.sexo_del_paciente)
        self.sexo_.place(x=95, y=268)

        # Botones
        self.boton_crear = tk.Button(self.marco2, width=50, pady=7, text='Crear registro', font=('Arial'), bg='#BE2623', fg='white', border=0, activebackground='#EAE8DC', command=self.habilitar_campos_crear)
        self.boton_crear.place(x=35, y=15)
        self.imagen_icono = PhotoImage(file='inicio_boton2.png')
        self.boton = tk.Button(self.marco_menu, width=221, height=80, text="       Inicio", image=self.imagen_icono,  compound="left", font=("Arial", 14), fg="#0E3746", bg="white", border=0, command=lambda: controller.mostrar_ventana(Ventana_2))
        self.boton.place(x=0, y=300)
        self.imagen_icono2 = PhotoImage(file='inicio_registros2.png')
        self.boton2 = tk.Button(self.marco_menu, width=221, height=80, text="    Registro", image=self.imagen_icono2,  compound="left", font=("Arial", 14), fg="#0E3746", bg="#EAE8DC", border=0, command=lambda: controller.mostrar_ventana(Ventana_3))
        self.boton2.place(x=0, y=400)

        self.boton_cerrar=tk.Button(self.marco_menu, width=18, pady=7, text='Cerrar sesión', font=('Arial'), bg='#BE2623', fg='white', border=0, activebackground='#EAE8DC', command=lambda: controller.mostrar_ventana(Ventana_1)).place(x=25, y=600)
        self.boton_crear=tk.Button(self.marco2, width=50, pady=7, text='Crear registro', font=('Arial'), bg='#BE2623', fg='white', border=0, activebackground='#EAE8DC', command=self.habilitar_campos_crear)
        self.boton_crear.place(x=35, y=15)

        self.boton_buscar_registro=tk.Button(self.marco2, width=50, pady=7, text='Buscar registro', font=('Arial'), bg='#0E3746', fg='white', border=0, activebackground='#EAE8DC', command=self.habilitar_campos_buscar)
        self.boton_buscar_registro.place(x=525, y=15)

        self.boton_guardar=tk.Button(self.marco2, width=50, pady=7, text='Guardar registro', font=('Arial'), bg='#17617B', fg='white', border=0, activebackground='#EAE8DC', command=self.deshabilitar_campos_guardar)
        self.boton_guardar.place(x=35, y=340)
        self.boton_buscar=tk.Button(self.marco2, width=50, pady=7, text='Buscar', font=('Arial'), bg='#17617B', fg='white', border=0, activebackground='#EAE8DC', command=self.deshabilitar_campos_buscar)
        self.boton_buscar.place(x=525, y=340)

    def habilitar_campos_crear(self):
        messagebox.showinfo("INFORMACIÓN IMPORTANTE", "*INSTRUCCIONES*, \n1.Ingrese el nombre completo: \n      Ejemplo: Itzel López Cárdenas \n \n2. Formato de fecha:  \n     Ejemplo: 13/04/2005 \n \n3. Creación usuario: \n   Iniciales en mayúsculas, fecha de nacimiento \n      Ejemplo: ILC13042005. \n \n4.Edad: \n       Ejemplo: 19 \n \n5. Sexo: \n        Ejemplo: Femenino")
        self.nombre_.config(state='normal')
        self.fecha_.config(state='normal')
        self.usuario_.config(state='normal')
        self.edad_.config(state='normal')
        self.sexo_.config(state='normal')
        self.boton_guardar.config(state='normal')
        self.boton_buscar.config(state='disabled')
        self.boton_buscar_registro.config(state='disabled')

    
    def deshabilitar_campos_guardar(self):
        self.nombre_.config(state='disabled')
        self.fecha_.config(state='disabled')
        self.usuario_.config(state='disabled')
        self.edad_.config(state='disabled')
        self.sexo_.config(state='disabled')
        self.boton_guardar.config(state='normal')
        self.boton_buscar.config(state='disabled')
        self.boton_crear.config(state='disabled')

        self.guardar()

    def habilitar_campos_buscar(self):
        messagebox.showinfo("INFORMACIÓN IMPORTANTE", "*INSTRUCCIONES*, \n1.Ingrese el usuario del paciente:  \n      Ejemplo: ILC13042005")
        self.nombre_.config(state='disabled')
        self.usuario_.config(state='normal')
        self.fecha_.config(state='disabled')
        self.edad_.config(state='disabled')
        self.sexo_.config(state='disabled')
        self.boton_guardar.config(state='disabled')
        self.boton_buscar.config(state='normal')
        self.boton_crear.config(state='disabled')
    
    def deshabilitar_campos_buscar(self):
        self.nombre_.config(state='disabled')
        self.usuario_.config(state='disabled')
        self.fecha_.config(state='disabled')
        self.edad_.config(state='disabled')
        self.sexo_.config(state='disabled')
        self.boton_guardar.config(state='disabled')
        self.boton_buscar.config(state='normal')
        self.boton_crear.config(state='disabled')

        self.buscar()


###########################################################################################################

    """ GUARDAR DATOS DEL PACIENTE """

    # GUARDAR ARCHIVO (TOMA LOS DATOS)
    def guardar(self):
        nombre_ = self.nombre_del_paciente.get().strip()
        fecha_ = self.fecha_de_nacimiento.get().strip()
        usuario_ = self.usuario_del_paciente.get().strip()
        edad_ = self.edad_del_paciente.get().strip()
        sexo_ = self.sexo_del_paciente.get().strip()

        if not nombre_ or not sexo_ or not usuario_:
            messagebox.showerror("ERROR", "Todos los campos deben estar completos.")
            return
        
        datos_paciente = {
            "Usuario": [usuario_],
            "Nombre": [nombre_],
            "Fecha de nacimiento": [fecha_],
            "Edad": [edad_],
            "Sexo": [sexo_]
        }
        df_paciente = pd.DataFrame(datos_paciente)
        usuario_archivo = f"{usuario_.replace('/', '_').replace('\\', '_').replace(':', '_').replace(' ', '_')}.csv"
        ruta_archivo = os.path.join(self.pacientes, usuario_archivo)
        try:
            df_paciente.to_csv(ruta_archivo, index=False)
            messagebox.showinfo("CONFIRMACIÓN", f"Paciente guardado como: {usuario_archivo}")
        except Exception as e:
            messagebox.showerror("ERROR", f"No se pudo guardar el archivo: {e}")

        self.monitoreo_guardar()

    # BUSQUEDA PARA AÑADIR
    def monitoreo_guardar(self):
        usuario = self.usuario_del_paciente.get()
        if not usuario:
            messagebox.showwarning("ERROR", "Por favor, ingrese un usuario.")
            return
        ruta_pacientes = self.pacientes
        archivo_buscado = None
        for archivo in os.listdir(ruta_pacientes):
            if archivo.endswith('.csv') and usuario in archivo:
                archivo_buscado = archivo
                break

        if archivo_buscado:
            self.monitoreo_guardar_(archivo_buscado)
            self.limpiar_datos()
            
    def limpiar_datos(self):
        self.nombre_del_paciente.set("")
        self.fecha_de_nacimiento.set("")
        self.usuario_del_paciente.set("")
        self.edad_del_paciente.set("")
        self.sexo_del_paciente.set("")
    
    def monitoreo_guardar_(self, archivo_buscado):
        usuario_pa = self.usuario_del_paciente.get()
        ventana_monitoreo = tk.Toplevel(self)
        ventana_monitoreo.title('HOJA GRÁFICA')  
        ventana_monitoreo.state("zoomed")
        ventana_monitoreo.configure(bg="#EAE8DC")
        ventana_monitoreo.iconbitmap('JYDHI_LOGO.ico')

        # Títulos y marcos
        titulo_inicio = tk.Label(ventana_monitoreo, text=f'REGISTRO DE SIGNOS VITALES   |   Bienvenido', fg='#BE2623', bg='#EAE8DC', font=('Arial', 24))
        titulo_inicio.place(x=35, y=30)
        marcos = tk.Frame(ventana_monitoreo, width=1290, height=50, bg='#17617B')
        marcos.place(x=35, y=100)
        marco2 = tk.Frame(ventana_monitoreo, width=1290, height=505, bg='white')
        marco2.place(x=35, y=170)
        marco3 = tk.Frame(ventana_monitoreo, width=572, height=65, bg='#BFE5F3')
        marco3.place(x=752, y=10)
        marcos_ = tk.Frame(ventana_monitoreo, width=1290, height=50, bg='#17617B')
        marcos_.place(x=35, y=575)

        # Gráfica dentro de marco2
        self.figura = Figure(figsize=(5, 3), dpi=100, facecolor="#FFFFFF")
        self.eje = self.figura.add_subplot(111)
        self.eje.set_facecolor("#F5F5F5")
        self.eje.set_title('Monitoreo de paciente', color="#17617B")
        self.eje.set_xlabel('Tiempo (s)', color="#17617B")
        self.eje.set_ylabel('Valor', color="#17617B")
        self.canvas = FigureCanvasTkAgg(self.figura, master=marco2)
        self.canvas.get_tk_widget().place(x=50, y=3, width=600, height=350)

        
        nombre = tk.Label(ventana_monitoreo, text=f'Usuario del paciente: {usuario_pa}', fg='white', bg='#17617B', font=('Arial', 14))
        nombre.place(x=50, y=110)
        instrucciones = tk.Label(ventana_monitoreo, text=f'INDICACIONES:', fg='#0E3746', bg='#BFE5F3', font=('Arial', 14))
        instrucciones.place(x=752, y=20)
        instrucciones_ = tk.Label(ventana_monitoreo, text=f'1. Registra los datos tal como aparecen en la pantalla.', fg='#0E3746', bg='#BFE5F3', font=('Arial', 8))
        instrucciones_.place(x=752, y=50)
        instrucciones_a = tk.Label(ventana_monitoreo, text=f'2. Una vez que hayas terminado de ingresar todos los datos de un signo vital, presiona "Guardar" para almacenarlos.', fg='#0E3746', bg='#BFE5F3', font=('Arial', 8))
        instrucciones_a.place(x=752, y=70)
        seleccion = tk.Label(ventana_monitoreo, text='SELECCIONE LA GRÁFICA QUE DESEA OBTENER', fg='white', bg='#17617B', font=('Arial', 14))
        seleccion.place(x=61, y=595)

        # BOTONES
        #fc = tk.Label(ventana_monitoreo, width=20, pady=5, text='ECG', font=("Arial", 11, "bold"), bg='#EAE8DC', fg='#0E3746', border=0)
        #fc.place(x=260, y=190)
        #fc = tk.Label(ventana_monitoreo, width=20, pady=5, text='FRECUENCIA CARDÍACA', font=("Arial", 11, "bold"), bg='#EAE8DC', fg='#0E3746', border=0)
        #fc.place(x=240, y=546)
        fc = tk.Label(ventana_monitoreo, width=24, pady=5, text='FRECUENCIA RESPIRATORIA', font=("Arial", 11, "bold"), bg='#EAE8DC', fg='#0E3746', border=0)
        fc.place(x=755, y=370)
        so = tk.Label(ventana_monitoreo, width=22, pady=5, text='SATURACIÓN DE OXÍGENO', font=("Arial", 11, "bold"), bg='#EAE8DC', fg='#0E3746', border=0)
        so.place(x=1075, y=370)
        ta = tk.Label(ventana_monitoreo, width=18, pady=5, text='TENSIÓN ARTERIAL',font=("Arial", 11, "bold"), bg='#EAE8DC', fg='#0E3746', border=0)
        ta.place(x=780, y=210)
        te = tk.Label(ventana_monitoreo, width=18, pady=5, text='TEMPERATURA',font=("Arial", 11, "bold"), bg='#EAE8DC', fg='#0E3746', border=0)
        te.place(x=1097, y=210)

        #################################
        tk.Button(ventana_monitoreo, width=22, pady=7, text='Frecuencia cardícaca', font=('Arial'), bg='#B3AC7F', fg='#0E3746', border=0, activebackground='white', command=lambda: self.fc_grafica(archivo_buscado)).place(x=61, y=630)
        tk.Button(ventana_monitoreo, width=22, pady=7, text='Temperatura', font=('Arial'), bg='#B3AC7F', fg='#0E3746', border=0, activebackground='white', command=lambda: self.t_grafica(archivo_buscado)).place(x=320, y=630)
        tk.Button(ventana_monitoreo, width=22, pady=7, text='Saturación de oxígeno', font=('Arial'), bg='#B3AC7F', fg='#0E3746', border=0, activebackground='white', command=lambda: self.so_grafica(archivo_buscado)).place(x=579, y=630)
        tk.Button(ventana_monitoreo, width=22, pady=7, text='Tensión arterial', font=('Arial'), bg='#B3AC7F', fg='#0E3746', border=0, activebackground='white', command=lambda: self.ta_grafica(archivo_buscado)).place(x=838, y=630)
        tk.Button(ventana_monitoreo, width=20, pady=7, text='Todas las gráficas', font=('Arial'), bg='#BE2623', fg='white', border=0, activebackground='white', command=lambda: self.todas_grafica(archivo_buscado)).place(x=1097, y=630)
        ################################

        tk.Button(ventana_monitoreo, width=25, pady=7, text='Guardar', font=('Arial'), bg='#BE2623', fg='white', border=0, activebackground='#EAE8DC', command=lambda: self.actualizar_datos(archivo_buscado)).place(x=760, y=500)
        tk.Button(ventana_monitoreo, width=25, pady=7, text='Salir', font=('Arial'), bg='#0E3746', fg='white', border=0, activebackground='#EAE8DC', cursor='hand2').place(x=1060, y=500)

        # Entradas
        self.fc = tk.StringVar()
        self.tas = tk.StringVar()
        self.tad = tk.StringVar()
        self.so = tk.StringVar()
        self.t = tk.StringVar()

        fc_en = tk.Entry(ventana_monitoreo, width=3, fg='#17617B', border=1, bg='white', font=('Arial', 25), textvariable=self.fc)
        fc_en.place(x=810, y=410)
        fc_lpm = tk.Label(ventana_monitoreo, width=5, pady=7, text='BPM', font=("Arial", 12), bg='white', fg='#17617B', border=0)
        fc_lpm.place(x=870, y=415)

        so_en = tk.Entry(ventana_monitoreo, width=3, fg='#17617B', border=1, bg='white', font=('Arial', 25), textvariable=self.so)
        so_en.place(x=1135, y=410)
        so_= tk.Label(ventana_monitoreo, width=5, pady=7, text='%', font=("Arial", 12), bg='white', fg='#17617B', border=0)
        so_.place(x=1195, y=415)

        ta_sisydias = tk.Label(ventana_monitoreo, width=30, pady=7, text='SISTÓLICA    /     DÍASTÓLICA', font=("Arial", 12), bg='white', fg='#17617B', border=0)
        ta_sisydias.place(x=725, y=250)
        ta_sis_en = tk.Entry(ventana_monitoreo, width=3, fg='#17617B', border=1, bg='white', font=('Arial', 25), textvariable=self.tas)
        ta_sis_en.place(x=775, y=285)
        ta_dias_en = tk.Entry(ventana_monitoreo, width=3, fg='#17617B', border=1, bg='white', font=('Arial', 25), textvariable=self.tad)
        ta_dias_en.place(x=895, y=285)
        ta_mmhg = tk.Label(ventana_monitoreo, width=5, fg='#17617B', text='mmHg', bg='white', font=('Arial', 10))
        ta_mmhg.place(x=842, y=300)

        te_en = tk.Entry(ventana_monitoreo, width=3, fg='#17617B', border=1, bg='white', font=('Arial', 25), textvariable=self.t)
        te_en.place(x=1135, y=260)
        te_= tk.Label(ventana_monitoreo, width=5, pady=7, text='ºC', font=("Arial", 12), bg='white', fg='#17617B', border=0)
        te_.place(x=1195, y=260)

        # Intentar abrir el puerto serial
        try:
            self.ser = serial.Serial('COM4', 9600)
            self.ser.flush()
            estado_conexion = "Conectado"  # Si se pudo conectar
        except serial.SerialException as e:
            estado_conexion = f"Error de conexión: {str(e)}"  # Mostrar el error si no se pudo conectar

        self.datos = []

        # Mostrar el estado de la conexión en una ubicación específica
        estado_label = tk.Label(ventana_monitoreo, text=estado_conexion, fg='red', bg='#EAE8DC', font=('Arial', 12, 'italic'))
        estado_label.place(x=350, y=180)
        self.actualizar_monitoreo()

    def guardar_datos(self, archivo_buscado):
        hora__fecha_actual = datetime.datetime.now().strftime('%d-%m-%Y / %H:%M:%S')

        fc = self.fc.get().strip()
        tas = self.tas.get().strip()
        tad = self.tad.get().strip()
        so = self.so.get().strip()
        t = self.t.get().strip()

        ruta_completa = os.path.join(self.pacientes, archivo_buscado)
        df_paciente = pd.read_csv(ruta_completa, encoding='utf-8')

        df_paciente['Hora y fecha'] = hora__fecha_actual
        df_paciente['Frecuencia cardiaca'] = fc
        df_paciente['Tension arterial sistolica'] = tas
        df_paciente['Tension arterial diastolica'] = tad
        df_paciente['Saturacion de oxigeno'] = so
        df_paciente['Temperatura'] = t

        df_paciente.to_csv(ruta_completa, index=False)
        messagebox.showinfo("CONFIRMACIÓN", f"Datos guardados correctamente para el usuario: {archivo_buscado}")

###########################################################################################

    """ ACTUALIZAR DATOS DEL PACIENTE """

    # BÚSQUEDA DEL USUARIO (SE INGRESA EL USUARIO)
    def buscar(self):
        usuario = self.usuario_del_paciente.get().strip()
        if not usuario:
            messagebox.showwarning("ERROR", "Por favor, ingrese un usuario.")
            return
        ruta_pacientes = self.pacientes
        archivo_buscado = None
        for archivo in os.listdir(ruta_pacientes):
            if archivo.endswith('.csv') and usuario in archivo:
                archivo_buscado = archivo
                break

        if archivo_buscado:
            messagebox.showinfo("ARCHIVO ENCONTRADO", f"Archivo encontrado: {archivo_buscado}")
            self.monitoreo_buscar(archivo_buscado)
            self.limpiar_usuario()

        else:
            messagebox.showerror("ARCHIVO NO ENCONTRADO", "No se encontró un archivo con ese usuario.")

    def monitoreo_buscar(self, archivo_buscado):
        usuario_pa = self.usuario_del_paciente.get()
        ventana_monitoreo = tk.Toplevel(self)
        ventana_monitoreo.title('HOJA GRÁFICA')  
        ventana_monitoreo.state("zoomed")
        ventana_monitoreo.configure(bg="#EAE8DC")
        ventana_monitoreo.iconbitmap('JYDHI_LOGO.ico')

        # Títulos y marcos
        titulo_inicio = tk.Label(ventana_monitoreo, text=f'REGISTRO DE SIGNOS VITALES   |   Bienvenido', fg='#BE2623', bg='#EAE8DC', font=('Arial', 24))
        titulo_inicio.place(x=35, y=30)
        marcos = tk.Frame(ventana_monitoreo, width=1290, height=50, bg='#17617B')
        marcos.place(x=35, y=100)
        marco2 = tk.Frame(ventana_monitoreo, width=1290, height=505, bg='white')
        marco2.place(x=35, y=170)
        marco3 = tk.Frame(ventana_monitoreo, width=572, height=65, bg='#BFE5F3')
        marco3.place(x=752, y=10)
        marcos_ = tk.Frame(ventana_monitoreo, width=1290, height=50, bg='#17617B')
        marcos_.place(x=35, y=575)

        # Gráfica dentro de marco2
        self.figura = Figure(figsize=(5, 3), dpi=100, facecolor="#FFFFFF")
        self.eje = self.figura.add_subplot(111)
        self.eje.set_facecolor("#F5F5F5")
        self.eje.set_title('Monitoreo de paciente', color="#17617B")
        self.eje.set_xlabel('Tiempo (s)', color="#17617B")
        self.eje.set_ylabel('Valor', color="#17617B")
        self.canvas = FigureCanvasTkAgg(self.figura, master=marco2)
        self.canvas.get_tk_widget().place(x=50, y=3, width=600, height=350)

        
        nombre = tk.Label(ventana_monitoreo, text=f'Usuario del paciente: {usuario_pa}', fg='white', bg='#17617B', font=('Arial', 14))
        nombre.place(x=50, y=110)
        instrucciones = tk.Label(ventana_monitoreo, text=f'INDICACIONES:', fg='#0E3746', bg='#BFE5F3', font=('Arial', 14))
        instrucciones.place(x=752, y=20)
        instrucciones_ = tk.Label(ventana_monitoreo, text=f'1. Registra los datos tal como aparecen en la pantalla.', fg='#0E3746', bg='#BFE5F3', font=('Arial', 8))
        instrucciones_.place(x=752, y=50)
        instrucciones_a = tk.Label(ventana_monitoreo, text=f'2. Una vez que hayas terminado de ingresar todos los datos de un signo vital, presiona "Guardar" para almacenarlos.', fg='#0E3746', bg='#BFE5F3', font=('Arial', 8))
        instrucciones_a.place(x=752, y=70)
        seleccion = tk.Label(ventana_monitoreo, text='SELECCIONE LA GRÁFICA QUE DESEA OBTENER', fg='white', bg='#17617B', font=('Arial', 14))
        seleccion.place(x=61, y=595)

        # BOTONES
        #fc = tk.Label(ventana_monitoreo, width=20, pady=5, text='ECG', font=("Arial", 11, "bold"), bg='#EAE8DC', fg='#0E3746', border=0)
        #fc.place(x=260, y=190)
        #fc = tk.Label(ventana_monitoreo, width=20, pady=5, text='FRECUENCIA CARDÍACA', font=("Arial", 11, "bold"), bg='#EAE8DC', fg='#0E3746', border=0)
        #fc.place(x=240, y=546)
        fc = tk.Label(ventana_monitoreo, width=24, pady=5, text='FRECUENCIA RESPIRATORIA', font=("Arial", 11, "bold"), bg='#EAE8DC', fg='#0E3746', border=0)
        fc.place(x=755, y=370)
        so = tk.Label(ventana_monitoreo, width=22, pady=5, text='SATURACIÓN DE OXÍGENO', font=("Arial", 11, "bold"), bg='#EAE8DC', fg='#0E3746', border=0)
        so.place(x=1075, y=370)
        ta = tk.Label(ventana_monitoreo, width=18, pady=5, text='TENSIÓN ARTERIAL',font=("Arial", 11, "bold"), bg='#EAE8DC', fg='#0E3746', border=0)
        ta.place(x=780, y=210)
        te = tk.Label(ventana_monitoreo, width=18, pady=5, text='TEMPERATURA',font=("Arial", 11, "bold"), bg='#EAE8DC', fg='#0E3746', border=0)
        te.place(x=1097, y=210)

        #################################
        tk.Button(ventana_monitoreo, width=22, pady=7, text='Frecuencia cardícaca', font=('Arial'), bg='#B3AC7F', fg='#0E3746', border=0, activebackground='white', command=lambda: self.fc_grafica(archivo_buscado)).place(x=61, y=630)
        tk.Button(ventana_monitoreo, width=22, pady=7, text='Temperatura', font=('Arial'), bg='#B3AC7F', fg='#0E3746', border=0, activebackground='white', command=lambda: self.t_grafica(archivo_buscado)).place(x=320, y=630)
        tk.Button(ventana_monitoreo, width=22, pady=7, text='Saturación de oxígeno', font=('Arial'), bg='#B3AC7F', fg='#0E3746', border=0, activebackground='white', command=lambda: self.so_grafica(archivo_buscado)).place(x=579, y=630)
        tk.Button(ventana_monitoreo, width=22, pady=7, text='Tensión arterial', font=('Arial'), bg='#B3AC7F', fg='#0E3746', border=0, activebackground='white', command=lambda: self.ta_grafica(archivo_buscado)).place(x=838, y=630)
        tk.Button(ventana_monitoreo, width=20, pady=7, text='Todas las gráficas', font=('Arial'), bg='#BE2623', fg='white', border=0, activebackground='white', command=lambda: self.todas_grafica(archivo_buscado)).place(x=1097, y=630)
        ################################

        tk.Button(ventana_monitoreo, width=25, pady=7, text='Guardar', font=('Arial'), bg='#BE2623', fg='white', border=0, activebackground='#EAE8DC', command=lambda: self.actualizar_datos(archivo_buscado)).place(x=760, y=500)
        tk.Button(ventana_monitoreo, width=25, pady=7, text='Salir', font=('Arial'), bg='#0E3746', fg='white', border=0, activebackground='#EAE8DC', cursor='hand2').place(x=1060, y=500)

        # Entradas
        self.fc = tk.StringVar()
        self.tas = tk.StringVar()
        self.tad = tk.StringVar()
        self.so = tk.StringVar()
        self.t = tk.StringVar()

        fc_en = tk.Entry(ventana_monitoreo, width=3, fg='#17617B', border=1, bg='white', font=('Arial', 25), textvariable=self.fc)
        fc_en.place(x=810, y=410)
        fc_lpm = tk.Label(ventana_monitoreo, width=5, pady=7, text='BPM', font=("Arial", 12), bg='white', fg='#17617B', border=0)
        fc_lpm.place(x=870, y=415)

        so_en = tk.Entry(ventana_monitoreo, width=3, fg='#17617B', border=1, bg='white', font=('Arial', 25), textvariable=self.so)
        so_en.place(x=1135, y=410)
        so_= tk.Label(ventana_monitoreo, width=5, pady=7, text='%', font=("Arial", 12), bg='white', fg='#17617B', border=0)
        so_.place(x=1195, y=415)

        ta_sisydias = tk.Label(ventana_monitoreo, width=30, pady=7, text='SISTÓLICA    /     DÍASTÓLICA', font=("Arial", 12), bg='white', fg='#17617B', border=0)
        ta_sisydias.place(x=725, y=250)
        ta_sis_en = tk.Entry(ventana_monitoreo, width=3, fg='#17617B', border=1, bg='white', font=('Arial', 25), textvariable=self.tas)
        ta_sis_en.place(x=775, y=285)
        ta_dias_en = tk.Entry(ventana_monitoreo, width=3, fg='#17617B', border=1, bg='white', font=('Arial', 25), textvariable=self.tad)
        ta_dias_en.place(x=895, y=285)
        ta_mmhg = tk.Label(ventana_monitoreo, width=5, fg='#17617B', text='mmHg', bg='white', font=('Arial', 10))
        ta_mmhg.place(x=842, y=300)

        te_en = tk.Entry(ventana_monitoreo, width=3, fg='#17617B', border=1, bg='white', font=('Arial', 25), textvariable=self.t)
        te_en.place(x=1135, y=260)
        te_= tk.Label(ventana_monitoreo, width=5, pady=7, text='ºC', font=("Arial", 12), bg='white', fg='#17617B', border=0)
        te_.place(x=1195, y=260)

        # Intentar abrir el puerto serial
        try:
            self.ser = serial.Serial('COM4', 9600)
            self.ser.flush()
            estado_conexion = "Conectado"  # Si se pudo conectar
        except serial.SerialException as e:
            estado_conexion = f"Error de conexión: {str(e)}"  # Mostrar el error si no se pudo conectar

        self.datos = []

        # Mostrar el estado de la conexión en una ubicación específica
        estado_label = tk.Label(ventana_monitoreo, text=estado_conexion, fg='red', bg='#EAE8DC', font=('Arial', 12, 'italic'))
        estado_label.place(x=350, y=180)
        self.actualizar_monitoreo()

    def actualizar_monitoreo(self):
        if hasattr(self, 'ser') and self.ser.is_open:  # Verificar si el puerto está abierto
            if self.ser.in_waiting > 0:
                datos_leidos = self.ser.readline().decode('utf-8').strip()
                self.datos.append(datos_leidos)
                if len(self.datos) > 50:
                    self.datos.pop(0)

                self.eje.clear()
                self.eje.plot(self.datos)
                self.eje.set_xlabel('Tiempo')
                self.eje.set_ylabel('Frecuencia')
                self.canvas.draw()

            self.after(1000, self.actualizar_monitoreo)
    
        def actualizar_valores():
            if ventana_monitoreo.ser.in_waiting > 0:
                linea = ventana_monitoreo.ser.readline().decode('utf-8').strip()
                busqueda = re.search(r'Heart rate:\s*([\d.]+)bpm\s*/\s*SpO2:\s*([\d]+)%', linea)
                if busqueda:
                    frecuencia_cardiaca = float(busqueda.group(1))
                    saturacion = float(busqueda.group(2))

                    for spine in ventana_monitoreo.ax1.spines.values():
                        spine.set_color('white')

                    # Cambiar el tamaño del texto de los ticks
                    ventana_monitoreo.ax1.tick_params(axis='x', labelsize=1, colors='white')
                    ventana_monitoreo.ax1.tick_params(axis='y', labelsize=10, colors='white')

                    ventana_monitoreo.ax1.clear()
                    ventana_monitoreo.ax1.bar(["Saturación de Oxígeno"], [saturacion], color='#17617B')
                    ventana_monitoreo.ax1.set_ylim(0, 100)

                    etiquetas[0]['text'] = f"{frecuencia_cardiaca:.2f} LPM"
                    etiquetas[1]['text'] = f"{saturacion:.2f}%"
                    ventana_monitoreo.canvas.draw()

            ventana_monitoreo.after(1, actualizar_valores)

        def cerrar_puerto():
            ventana_monitoreo.ser.close()
            ventana_monitoreo.destroy()

        ventana_monitoreo.protocol("WM_DELETE_WINDOW", cerrar_puerto)
        actualizar_valores()

    # ABRE EL ARCHIVO Y AÑADE FILAS
    def actualizar_datos(self, archivo_buscado):
        hora__fecha_actual = datetime.datetime.now().strftime('%d-%m-%Y / %H:%M:%S')

        fc = self.fc.get().strip()
        tas = self.tas.get().strip()
        tad = self.tad.get().strip()
        so = self.so.get().strip()
        t = self.t.get().strip()

        ruta_completa = os.path.join(self.pacientes, archivo_buscado)
        df_paciente = pd.read_csv(ruta_completa, encoding='utf-8')

        # Crear un DataFrame temporal con la nueva fila
        nueva_fila = pd.DataFrame([{
            'Hora y fecha': hora__fecha_actual,
            'Frecuencia cardiaca': fc,
            'Tension arterial sistolica': tas,
            'Tension arterial diastolica': tad,
            'Saturacion de oxigeno': so,
            'Temperatura': t
        }])
        
        df_paciente = pd.concat([df_paciente, nueva_fila], ignore_index=True)

        df_paciente.to_csv(ruta_completa, index=False)
        messagebox.showinfo("CONFIRMACIÓN", f"Datos guardados correctamente para el usuario: {archivo_buscado}")

    # LIMPIAR LOS CAMPOS DE LA VENTANA PRINCIPAL
    def limpiar_usuario(self):
        self.usuario_del_paciente.set("")

#############################################################################################

    """ HOJA GRÁFICA """

    # BÚSQUEDA DEL USUARIO
    def graficar(self):
        usuario = self.usuario_del_paciente.get()
        if not usuario:
            messagebox.showwarning("ERROR", "Por favor, ingrese un usuario.")
            return
        ruta_pacientes = self.pacientes
        archivo_buscado = None
        for archivo in os.listdir(ruta_pacientes):
            if archivo.endswith('.csv') and usuario in archivo:
                archivo_buscado = archivo
                break

        if archivo_buscado:
            messagebox.showinfo("ARCHIVO ENCONTRADO", f"Archivo encontrado: {archivo_buscado}")
            self.ventana_graficar(archivo_buscado)

        else:
            messagebox.showerror("ARCHIVO NO ENCONTRADO", "No se encontró un archivo con ese usuario.")

    # VENTANA GRAFICA    
    def fc_grafica(self, archivo_buscado):
        ruta_completa = os.path.join(self.pacientes, archivo_buscado)
        df_paciente = pd.read_csv(ruta_completa, encoding='utf-8')
        df_paciente.head()

        if "Hora y fecha" in df_paciente.columns and "Frecuencia cardiaca" in df_paciente.columns:
            df_paciente["Hora y fecha"] = pd.to_datetime(df_paciente["Hora y fecha"], errors='coerce')
            df_paciente = df_paciente.dropna(subset=["Hora y fecha"])

            plt.figure(figsize=(12, 6))
            plt.plot(df_paciente["Hora y fecha"], df_paciente["Frecuencia cardiaca"], marker='o', label="Frecuencia Cardíaca", color="blue")
            plt.title("Frecuencia Cardíaca", fontsize=14)
            for x, y in zip(df_paciente["Hora y fecha"], df_paciente["Frecuencia cardiaca"]):
                plt.text(x, y, f'{x.strftime("%d-%m-%Y  /  %H:%M:%S")} - {y:.0f}', fontsize=8, ha='right', va='bottom', color="black")
            plt.xlabel("Hora y fecha", fontsize=12)
            plt.ylabel("Frecuencia Cardíaca (bpm)", fontsize=12)
            plt.xticks(rotation=45)
            plt.grid()
            plt.legend()
            plt.tight_layout()
            plt.show()
        else:
            print("El archivo no contiene las columnas 'Hora y fecha' y/o 'Frecuencia_Cardiaca'.")
    
    
    # GRAFICA SATURACIÓN DE OXIGENO
    def so_grafica(self, archivo_buscado):
        ruta_completa = os.path.join(self.pacientes, archivo_buscado)
        df_paciente = pd.read_csv(ruta_completa, encoding='utf-8')
        df_paciente.head()

        if "Hora y fecha" in df_paciente.columns and "Saturacion de oxigeno" in df_paciente.columns:
            df_paciente["Hora y fecha"] = pd.to_datetime(df_paciente["Hora y fecha"], errors='coerce')
            df_paciente = df_paciente.dropna(subset=["Hora y fecha"])

            plt.figure(figsize=(12, 6))
            plt.plot(df_paciente["Hora y fecha"], df_paciente["Saturacion de oxigeno"], marker='o', label="Saturacion de oxigeno", color="red")
            plt.title("Saturacion de oxigeno", fontsize=14)
            for x, y in zip(df_paciente["Hora y fecha"], df_paciente["Saturacion de oxigeno"]):
                plt.text(x, y, f'{x.strftime("%d-%m-%Y  /  %H:%M:%S")} - {y:.0f}', fontsize=8, ha='right', va='bottom', color="black")
            plt.xlabel("Hora y fecha", fontsize=12)
            plt.ylabel("Saturacion de oxigeno (%)", fontsize=12)
            plt.xticks(rotation=45)
            plt.grid()
            plt.legend()
            plt.tight_layout()
            plt.show()
        else:
            print("El archivo no contiene las columnas 'Hora y fecha' y/o 'Saturacion de oxigeno'.")

    # GRAFICA TEMPERATURA
    def t_grafica(self, archivo_buscado):
        ruta_completa = os.path.join(self.pacientes, archivo_buscado)
        df_paciente = pd.read_csv(ruta_completa, encoding='utf-8')
        df_paciente.head()

        if "Hora y fecha" in df_paciente.columns and "Temperatura" in df_paciente.columns:
            df_paciente["Hora y fecha"] = pd.to_datetime(df_paciente["Hora y fecha"], errors='coerce')
            df_paciente = df_paciente.dropna(subset=["Hora y fecha"])

            plt.figure(figsize=(12, 6))
            plt.plot(df_paciente["Hora y fecha"], df_paciente["Temperatura"], marker='o', label="Temperatura", color="red")
            plt.title("Temperatura", fontsize=14)
            for x, y in zip(df_paciente["Hora y fecha"], df_paciente["Temperatura"]):
                plt.text(x, y, f'{x.strftime("%d-%m-%Y  /  %H:%M:%S")} - {y:.0f}', fontsize=8, ha='right', va='bottom', color="black")
            plt.xlabel("Hora y fecha", fontsize=12)
            plt.ylabel("Temperatura (ºC)", fontsize=12)
            plt.xticks(rotation=45)
            plt.grid()
            plt.legend()
            plt.tight_layout()
            plt.show()
        else:
            print("El archivo no contiene las columnas 'Hora' y/o 'Temperatura'.")

    # GRAFICA TENSIÓN ARTERIAL
    def ta_grafica(self, archivo_buscado):
        ruta_completa = os.path.join(self.pacientes, archivo_buscado)
        df_paciente = pd.read_csv(ruta_completa, encoding='utf-8')
        df_paciente.head()

        if "Hora y fecha" in df_paciente.columns and "Tension arterial sistolica" in df_paciente.columns and "Tension arterial diastolica" in df_paciente.columns:
            df_paciente["Hora y fecha"] = pd.to_datetime(df_paciente["Hora y fecha"], errors='coerce')
            df_paciente = df_paciente.dropna(subset=["Hora y fecha"])

            plt.figure(figsize=(12, 6))
            plt.plot(df_paciente["Hora y fecha"], df_paciente["Tension arterial sistolica"], marker='o', label="Tensión arterial", color="red")
            plt.plot(df_paciente["Hora y fecha"], df_paciente["Tension arterial diastolica"], marker='o', label="Tensión arterial", color="blue")
            plt.title("Tensión arterial", fontsize=14)

            for x, y in zip(df_paciente["Hora y fecha"], df_paciente["Tension arterial sistolica"]):
                plt.text(x, y, f'{x.strftime("%d-%m-%Y  /  %H:%M:%S")} - {y:.0f}', fontsize=8, ha='right', va='bottom', color="black")
            for x, y in zip(df_paciente["Hora y fecha"], df_paciente["Tension arterial diastolica"]):
                plt.text(x, y, f'{x.strftime("%d-%m-%Y  /  %H:%M:%S")} - {y:.0f}', fontsize=8, ha='right', va='bottom', color="black")

            plt.xlabel("Hora y fecha", fontsize=12)
            plt.ylabel("Tensión arterial", fontsize=12)
            plt.xticks(rotation=45)
            plt.grid()
            plt.legend()
            plt.tight_layout()
            plt.show()
        else:
            print("El archivo no contiene las columnas 'Hora y fecha' y/o 'Tension arterial sistolica'.")

    # TODAS LAS GRÁFICAS
    def todas_grafica(self, archivo_buscado):
        self.fc_grafica(archivo_buscado)
        self.so_grafica(archivo_buscado)
        self.t_grafica(archivo_buscado)
        self.ta_grafica(archivo_buscado)
if __name__ == "__main__":
    app = JYDHI()
    app.mainloop()
