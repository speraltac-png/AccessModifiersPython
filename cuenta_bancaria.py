class CuentaBancaria:
	"""Cuenta bancaria con atributos público, protegido y privado.

	- numero_cuenta: público
	- _saldo: protegido (convención)
	- __pin: privado (name mangling)

	Se usan properties y métodos para encapsular el acceso.
	"""

	def __init__(self, numero_cuenta, pin_inicial, saldo_inicial = 0.0):
		self.numero_cuenta = numero_cuenta  # público
		self._saldo = 0.0  # protegido por convención
		self.__pin = ""  # privado
		self._validar_monto(saldo_inicial)
		self._saldo = float(saldo_inicial)
		self.__establecer_pin_inicial(pin_inicial)

	@property
	def saldo(self):
		"""Saldo de solo lectura desde fuera; modificado por métodos públicos."""
		return self._saldo

	def depositar(self, monto):
		self._validar_monto(monto)
		self._saldo += float(monto)

	def retirar(self, monto, pin):
		self._validar_monto(monto)
		self._requerir_pin(pin)
		if monto > self._saldo:
			raise ValueError("Fondos insuficientes")
		self._saldo -= float(monto)

	def transferir_a(self, destino, monto, pin):
		self.retirar(monto, pin)
		destino.depositar(monto)

	def consultar_saldo(self):
		return self.saldo

	def cambiar_pin(self, pin_actual, pin_nuevo):
		self._requerir_pin(pin_actual)
		self._validar_pin_formato(pin_nuevo)
		self.__pin = pin_nuevo

	# ----------------------- Métodos "protegidos" -----------------------
	def _validar_monto(self, monto):
		if not isinstance(monto, (int, float)):
			raise TypeError("El monto debe ser numérico")
		if monto <= 0:
			raise ValueError("El monto debe ser positivo")

	def _requerir_pin(self, pin):
		if pin != self.__pin:
			raise PermissionError("PIN incorrecto")

	def _validar_pin_formato(self, pin):
		if not isinstance(pin, str) or len(pin) < 4 or not pin.isdigit():
			raise ValueError("El PIN debe tener al menos 4 dígitos")

	# ----------------------- Métodos "privados" -------------------------
	def __establecer_pin_inicial(self, pin_inicial):
		self._validar_pin_formato(pin_inicial)
		self.__pin = pin_inicial



