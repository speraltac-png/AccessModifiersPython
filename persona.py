class Persona:
	"""Representa una persona con atributos público, protegido y privado.

	- nombre: público
	- _dni: protegido (convención)
	- __edad: privado (name mangling)
	"""

	def __init__(self, nombre, dni, edad):
		self.nombre = nombre  # público
		self._dni = dni  # protegido por convención
		self.__edad = 0  # privado (name mangling)
		#self.edad = edad  # usa property para validar

	@property
	def edad(self):
		"""Getter controlado para edad (accede al atributo privado)."""
		return self.__edad

	@edad.setter
	def edad(self, valor):
		"""Setter con validación para el atributo privado __edad."""
		if not isinstance(valor, int):
			raise TypeError("La edad debe ser un entero")
		if valor < 0:
			raise ValueError("La edad no puede ser negativa")
		self.__edad = valor

	def presentarse(self):
		return f"Hola, soy {self.nombre} y tengo {self.__edad} años."


