import sqlite3
from tkinter import *
from tkinter import messagebox

raiz = Tk()
raiz.title("Usuarios")
raiz.resizable(0,0)

frame = Frame(raiz)
frame.pack()

#*************************************Variables*************************************#

varId = StringVar()
varNombre = StringVar()
varPassword = StringVar()
varApellido = StringVar()
varDireccion = StringVar()

#*************************************Validacion*************************************#

def validacion(opcion):
	if opcion == "crear":
		return True

	elif opcion == "leer" or opcion == "borrar":
		return varId.get() != ""
		
	if varNombre.get() != "" and varPassword.get() != "" and varApellido.get() != "" and varDireccion.get() != "" and comentariosText.get(1.0, END) != "" and opcion == "insertar":
		return True

	elif varNombre.get() != "" and varPassword.get() != "" and varApellido.get() != "" and varDireccion.get() != "" and comentariosText.get(1.0, END) != "" and opcion == "actualizar" and varId.get() != "":
		return True

	else :
		return False

#*************************************Borrar*************************************#

def borrar():
	varId.set("")
	varNombre.set("")
	varPassword.set("")
	varApellido.set("")
	varDireccion.set("")
	comentariosText.delete(1.0, END)

#*************************************Salir*************************************#

def salir():
	salir = messagebox.askyesno("Salir", "¿Deseas salir de la aplicación?")

	if salir:
		raiz.destroy()

#*************************************BorrarBD*************************************#

def borrarBD():
	conexion = sqlite3.connect("Usuarios")
	cursor = conexion.cursor()

	limpiar = messagebox.askyesno("Borrar", "¿Deseas limpiar la BBDD?")

	if limpiar:
		cursor.execute("DELETE FROM DATOSUSUARIOS")
		cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'DATOSUSUARIOS'")
		messagebox.showinfo("BBDD", "Se ha limpiado la BBDD")

	conexion.commit()
	cursor.close()
	conexion.close()

#*************************************conectarBD*************************************#

def conectarBD(opcion):
	conexion = sqlite3.connect("Usuarios")
	cursor = conexion.cursor()

	if validacion(opcion):

		if opcion == "crear":

			try :
				cursor.execute('''CREATE TABLE DATOSUSUARIOS (
					ID INTEGER PRIMARY KEY AUTOINCREMENT,
					NOMBRE_USUARIO VARCHAR(50),
					PASSWORD VARCHAR(50),
					APELLIDO VARCHAR(10),
					DIRECCION VARCHAR(50),
					COMENTARIOS VARCHAR(100) ) 
				''')

				messagebox.showinfo("BBDD", "BBDD creada con éxito")

			except:
				messagebox.showwarning("¡Atención!", "La BBDD ya existe")

		elif opcion == "insertar":
		 
			nombre = varNombre.get()
			password = varPassword.get()
			apellido = varApellido.get()
			direccion = varDireccion.get()
			comentarios = comentariosText.get(1.0, END)

			usuarioDatos = [
				(nombre, password, apellido, direccion,comentarios)
			]

			cursor.executemany("INSERT INTO DATOSUSUARIOS VALUES(NULL,?,?,?,?,?)", usuarioDatos)

			messagebox.showinfo("BBDD","Registro insertado con éxito")
			borrar()

		elif opcion == "leer":

			buscarID = int(varId.get())

			cursor.execute("SELECT * FROM DATOSUSUARIOS WHERE ID = {}".format(buscarID))
			usuarioDatos = cursor.fetchall()

			for i in usuarioDatos:
				varNombre.set(i[1])
				varPassword.set(i[2])
				varApellido.set(i[3])
				varDireccion.set(i[4])
				comentariosText.delete(1.0, END)
				comentariosText.insert(INSERT, i[5])

		elif opcion == "actualizar":

			buscarID = int(varId.get())

			nombre = varNombre.get()
			password = varPassword.get()
			apellido = varApellido.get()
			direccion = varDireccion.get()
			comentarios = comentariosText.get(1.0, END)

			usuarioDatos = [
				(nombre, password, apellido, direccion,comentarios, buscarID)
			]

			cursor.executemany("UPDATE DATOSUSUARIOS SET NOMBRE_USUARIO = ?, PASSWORD = ?, APELLIDO = ?, DIRECCION = ?, COMENTARIOS = ? WHERE ID = ?", usuarioDatos)
			messagebox.showinfo("BBDD", "Registro actualizado con éxito")
			borrar()

		elif opcion == "borrar":

			buscarID = int(varId.get())
			cursor.execute("DELETE FROM DATOSUSUARIOS WHERE ID = {}".format(buscarID))
			messagebox.showinfo("BBDD", "Registro borrado con éxito")
			borrar()
	else :
		messagebox.showwarning("¡Atención!", "No pueden haber espacios en blanco")

	conexion.commit()
	cursor.close()
	conexion.close()

#*************************************BARRA MENU*************************************#

barraMenu = Menu(raiz)
raiz.config(menu = barraMenu)

bdMenu = Menu(barraMenu, tearoff = 0)
bdMenu.add_command(label = "Conectar", command = lambda: conectarBD("crear"))
bdMenu.add_command(label = "Limpiar", command = borrarBD)
bdMenu.add_command(label = "Salir", command = salir)

borrarMenu = Menu(barraMenu, tearoff = 0)
borrarMenu.add_command(label = "Borrar campos", command = borrar)

crudMenu = Menu(barraMenu, tearoff = 0)
crudMenu.add_command(label = "Crear", command = lambda: conectarBD("insertar"))
crudMenu.add_command(label = "Leer", command = lambda: conectarBD("leer"))
crudMenu.add_command(label = "Actualizar", command = lambda: conectarBD("actualizar"))
crudMenu.add_command(label = "Borrar", command = lambda: conectarBD("borrar"))

ayudaMenu = Menu(barraMenu, tearoff = 0)
ayudaMenu.add_command(label = "Acerca de", command = lambda: messagebox.showinfo("Acerca de", "Programa Realizado por Jeremy664K\n        	Para el curso de\n            Pildoras Informaticas"))
ayudaMenu.add_command(label = "Licencia", command = lambda: messagebox.showinfo("Licencia", "*** Software publico si se dan Creditos a \nPildoras Informaticas ***"))

barraMenu.add_cascade(label = "BBDD", menu = bdMenu)
barraMenu.add_cascade(label = "Borrar", menu = borrarMenu)
barraMenu.add_cascade(label = "CRUD", menu = crudMenu)
barraMenu.add_cascade(label = "Ayuda", menu = ayudaMenu)

#*************************************Design Interfaz*************************************#

Label(frame, text = "Id:", font = ("Roboto", 10)).grid(row = 0, column = 0, pady = 10, padx = 10)
Entry(frame, font = ("Roboto",9), textvariable = varId).grid(row = 0, column = 1, pady = 10, padx = 10)

Label(frame, text = "Nombre:", font = ("Roboto", 10)).grid(row = 1, column = 0, pady = 10, padx = 10)
Entry(frame, font = ("Roboto",9), fg = "red", justify = "right", textvariable = varNombre).grid(row = 1, column = 1, pady = 10, padx = 10)

Label(frame, text = "Password:", font = ("Roboto", 10)).grid(row = 2, column = 0, pady = 10, padx = 10)
Entry(frame, font = ("Roboto",9), show = "?", textvariable = varPassword).grid(row = 2, column = 1, pady = 10, padx = 10)

Label(frame, text = "Apellido:", font = ("Roboto", 10)).grid(row = 3, column = 0, pady = 10, padx = 10)
Entry(frame, font = ("Roboto",9), textvariable = varApellido).grid(row = 3, column = 1, pady = 10, padx = 10)

Label(frame, text = "Direccion:", font = ("Roboto", 10)).grid(row = 4, column = 0, pady = 10, padx = 10)
Entry(frame, font = ("Roboto",9), textvariable = varDireccion).grid(row = 4, column = 1, pady = 10, padx = 10)

Label(frame, text = "Comentarios:", font = ("Roboto", 10)).grid(row = 5, column = 0, pady = 10, padx = 10)

comentariosText = Text(frame, width = 16, height = 5,font = ("Roboto"))
comentariosText.grid(row = 5, column = 1, pady = 10, padx = 10)
scrollVelt = Scrollbar(frame, command = comentariosText.yview)
scrollVelt.grid(row = 5, column = 2, sticky = "nsew")
comentariosText.config(yscrollcommand = scrollVelt.set)

Button(raiz, text = "Create", font = ("Roboto", 10), command = lambda: conectarBD("insertar")).pack(side = "left", padx = 10, pady = 10)
Button(raiz, text = "Read", font = ("Roboto", 10), command = lambda: conectarBD("leer")).pack(side = "left", padx = 10, pady = 10)
Button(raiz, text = "Update", font = ("Roboto", 10), command = lambda: conectarBD("actualizar")).pack(side = "left", padx = 10, pady = 10)
Button(raiz, text = "Delete", font = ("Roboto", 10), command = lambda: conectarBD("borrar")).pack(side = "left", padx = 10, pady = 10)

raiz.mainloop()