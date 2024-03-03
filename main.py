import re
import mysql.connector
from mysql.connector import Error
from os import system
table = "test"

class Persona():
	id_persona = ""
	nombre = ""
	apellidoPaterno = ""
	apellidoMaterno = ""
	cedula = ""
	especialidad = ""
	consultorio = ""
	telefono =  ""
	precio = ""
	universidad = ""
	def __init__(self):	
		a = ""
	
		
class interfaz():
	mensajeBienvenida =  """
		1 Para insertar
		2 Para borrar
		3 Para consultar todos
		4 Para actualizar
		5 Para filtrar por especialidad
		6 Para filtrar por maximo de precio
		0 Para salir
		"""
	
	inputLine = ""
	
	def __init__(self, table):
		self.table = table
		dropQuery = "DROP TABLE persona;"
		createQuery = """
			CREATE TABLE IF NOT EXISTS persona(
			id_persona serial PRIMARY KEY,
			nombre VARCHAR ( 50 ),
			apellidoPaterno VARCHAR ( 50 ),
			apellidoMaterno VARCHAR ( 50 ),
			cedula VARCHAR ( 50 ),
			especialidad VARCHAR ( 50 ),
			consultorio VARCHAR ( 50 ),
			telefono VARCHAR ( 50 ),
			precio FLOAT (15, 2),
			universidad VARCHAR ( 50 )
			);
			"""
		self.ejecutarConsulta(dropQuery)
		self.ejecutarConsulta(createQuery)

		
	def hasNext(self):
		return (self.inputLine != "")
	def next(self):
		self.inputLine = input()
	def  capturarString(self):
		self.next()
		while(not(self.hasNext())):
			print("Cadena inválida")
			self.next()
		return self.inputLine
	def  capturarDigito(self):
		self.next()
		while(not(self.inputLine.isdigit())):
			print("Numero inválido")
			self.next()
		return self.inputLine
	def capturarTelefono(self):
		self.next()
		foundedMatch = None
		while(not(self.inputLine.isdigit()) or (foundedMatch == None) or (not(foundedMatch.group(0) == self.inputLine))):
			print("Telefono inválido")
			self.next()
			foundedMatch = re.search("^\\+?[1-9][0-9]{7,14}$", self.inputLine)
		return self.inputLine
	def iniciarMenu(self):
		terminar = False
		first = True
		while((not terminar) or first):
			if(first): first = False

			print(self.mensajeBienvenida)
			self.next()
			if(self.inputLine == "1"):
				self.insertar(self.capturarPersona())
				
			elif(self.inputLine == "2"):
				self.borrar(self.capturarId())
				print(self.inputLine)
				
			elif(self.inputLine == "3"):
				self.consultarTodos()
				print(self.inputLine)
				
			elif(self.inputLine == "4"):
				self.actualizar(self. capturarPersona())
				print(self.inputLine)
			elif(self.inputLine == "5"):
				self.filtrarEspecialidad(self.capturarEspecialidad())
				print(self.inputLine)
			elif(self.inputLine == "6"):
				self.filtrarPrecio(self.capturarPrecio())
				print(self.inputLine)
				
			elif(self.inputLine == "0"):
				terminar = True
				print(self.inputLine)
			else:
				print("Entrada invalida")
				print(self.mensajeBienvenida)
			print("Presione enter para continuar")
			self.next()
			system('clear')

	def capturarPersona(self):
		print("Inserte el id del doctor:")
		id_persona = self.capturarDigito()
		print("Inserta el nombre del doctor:")
		nombre = self.capturarString()
		print("Inserta el apellido paterno del doctor:")
		apellidoPaterno = self.capturarString()
		print("Inserta el apellido materno del doctor:")
		apellidoMaterno = self.capturarString()
		print("Inserta la cedula del doctor:")
		cedula = self.capturarString()
		print("Inserta la especialidad del doctor:")
		especialidad = self.capturarString()
		print("Inserta el consultorio del doctor:")
		consultorio = self.capturarString()
		print("Inserta el telefono del doctor:")
		telefono = self.capturarTelefono()
		print("Inserta el precio de la consulta del doctor:")
		precio = self.capturarDigito()
		print("Inserta la universidad de origen del doctor:")
		universidad = self.capturarString()

		persona = Persona()
		persona.id_persona = id_persona
		persona.nombre = nombre
		persona.apellidoPaterno = apellidoPaterno
		persona.apellidoMaterno = apellidoMaterno
		persona.cedula = cedula
		persona.especialidad = especialidad
		persona.consultorio = consultorio
		persona.telefono = telefono
		persona.precio = precio
		persona.universidad = universidad

		return persona
	def capturarId(self):
		print("Inserte el id")
		return self.capturarDigito()
	def capturarEspecialidad(self):
		print("Inserte la especialidad a buscar")
		return self.capturarString()
	def capturarPrecio(self):
		print("Inserte el precio a buscar")
		return self.capturarDigito()
	
	def ejecutarConsulta(self, consulta):
		try:
			connection = mysql.connector.connect(
							host='database',
							database='test',
							user='my_user',
							password='my_password',
							autocommit=True)
			cursor = connection.cursor()
			cursor.execute(consulta)
			for x in cursor:
			  print(x) 
		except Error as e:
			print("Error while connecting to MySQL", e)
		 
		if connection.is_connected():
			connection.close()
			cursor.close() 
			print("MySQL connection is closed") 		
	def desplegarMenu():
		print(mensajeBienvenida)
	def insertar(self, persona):
		nombre = persona.nombre
		apellidoPaterno = persona.apellidoPaterno
		apellidoMaterno = persona.apellidoMaterno
		cedula = persona.cedula 
		especialidad = persona.especialidad 
		consultorio = persona.consultorio 
		telefono = persona.telefono 
		precio = persona.precio 
		universidad = persona.universidad 
		consulta = """
					INSERT INTO {table}(
										nombre,
										apellidoPaterno,
										apellidoMaterno,
										cedula,
										especialidad,
										consultorio,
										telefono,
										precio,
										universidad
										)
								VALUES (
										\"{nombre}\",
										\"{apellidoPaterno}\",
										\"{apellidoMaterno}\",
										\"{cedula}\",
										\"{especialidad}\",
										\"{consultorio}\",
										\"{telefono}\",
										\"{precio}\",
										\"{universidad}\"
										);
					""".format(
			table =  self.table,
			nombre = nombre,
			apellidoPaterno = apellidoPaterno,
			apellidoMaterno = apellidoMaterno,
			cedula = persona.cedula,
			especialidad = especialidad,
			consultorio = consultorio,
			telefono = telefono,
			precio = precio,
			universidad = universidad
			)
		print(consulta)
		self.ejecutarConsulta(consulta)
	def borrar(self, id_persona):
		consulta = "DELETE FROM {table} WHERE (id_persona={id_persona});".format(
			table =  self.table,
			id_persona = id_persona)
		print(consulta)
		self.ejecutarConsulta(consulta)
	def actualizar(self, persona):
		id_persona = persona.id_persona
		nombre = persona.nombre
		apellidoPaterno = persona.apellidoPaterno
		apellidoMaterno = persona.apellidoMaterno
		cedula = persona.cedula 
		especialidad = persona.especialidad 
		consultorio = persona.consultorio 
		telefono = persona.telefono 
		precio = persona.precio 
		universidad = persona.universidad 
		consulta = """
		UPDATE {table} 
		SET
		 nombre = \"{nombre}\",
		 apellidoPaterno = \"{apellidoPaterno}\", 
		 apellidoMaterno = \"{apellidoMaterno}\",
		 cedula = \"{cedula}\",
		 especialidad = \"{especialidad}\",
		 consultorio = \"{consultorio}\",
		 telefono = \"{telefono}\",
		 precio = \"{precio}\",
		 universidad = \"{universidad}\"
		WHERE
		 id_persona = \"{id_persona}\";
		 """.format(
			table =  self.table,
			nombre = nombre,
			apellidoPaterno = apellidoPaterno,
			apellidoMaterno = apellidoMaterno,
			cedula = persona.cedula,
			especialidad = especialidad,
			consultorio = consultorio,
			telefono = telefono,
			precio = precio,
			universidad = universidad,
			id_persona = id_persona
			)
			   
		print(consulta)
		self.ejecutarConsulta(consulta)
	def consultarTodos(self):
		consulta = """
		SELECT * FROM {table}
		""".format(table = self.table)
		print(consulta)
		self.ejecutarConsulta(consulta)
	def filtrarEspecialidad(self, especialidad):
		consulta = """
		SELECT * FROM {table}
		WHERE "\{especialidad}\"
		""".format(
			table = self.table,
			especialidad = especialidad
			)
		print(consulta)
		self.ejecutarConsulta(consulta)
	def filtrarPrecio(self, precio):
		consulta = """
		SELECT * FROM {table}
		WHERE precio < {precio}
		""".format(table = self.table,
					precio = precio
				)
		print(consulta)
		self.ejecutarConsulta(consulta)

		

		
	
interfazPrincipal = interfaz("persona")
interfazPrincipal.iniciarMenu()
