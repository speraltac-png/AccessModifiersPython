from persona import Persona
from cuenta_bancaria import CuentaBancaria


class OficinaBancaria:
	"""Orquesta acciones entre personas y cuentas.

	- nombre: público
	- _cuentas: protegido (convención)
	- __fondos_reserva: privado (sólo interno)
	"""

	def __init__(self, nombre):
		self.nombre = nombre
		self._cuentas = {}
		self.__fondos_reserva = 0.0

	def abrir_cuenta(self, persona, numero_cuenta, pin_inicial, deposito_inicial = 0.0):
		if numero_cuenta in self._cuentas:
			raise ValueError("El número de cuenta ya existe")
		cuenta = CuentaBancaria(numero_cuenta, pin_inicial, deposito_inicial)
		self._cuentas[numero_cuenta] = cuenta
		self.__fondos_reserva += max(0.0, deposito_inicial) * 0.01  # 1% a reserva interna
		return cuenta

	def obtener_cuenta(self, numero_cuenta):
		cuenta = self._cuentas.get(numero_cuenta)
		if cuenta is None:
			raise KeyError("Cuenta no encontrada")
		return cuenta

	def transferir(self, origen, destino, monto, pin_origen):
		cuenta_origen = self.obtener_cuenta(origen)
		cuenta_destino = self.obtener_cuenta(destino)
		cuenta_origen.transferir_a(cuenta_destino, monto, pin_origen)

	def total_depositado(self):
		return sum(c.saldo for c in self._cuentas.values())

	def _resumen_interno(self):
		return f"Reservas internas: {self.__fondos_reserva:.2f} | Cuentas: {len(self._cuentas)}"



