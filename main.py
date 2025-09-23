from persona import Persona
from cuenta_bancaria import CuentaBancaria
from oficina import OficinaBancaria


def mostrar_encabezado(texto):
	print("\n" + "=" * 72)
	print(texto)
	print("=" * 72)


def demo_persona():
	mostrar_encabezado("Demostración: Persona (público, protegido, privado)")
	persona = Persona(nombre="Ana", dni="12345678X", edad=30)

	print("Nombre (público):", persona.nombre)
	print("Edad via property (privado con property):", persona.edad)
	print("Presentación:", persona.presentarse())

	print("_dni (protegido, por convención):", persona._dni)

	try:
		print(persona.__edad)
	except AttributeError as e:
		print("Acceso directo a __edad (privado) -> ERROR ESPERADO:", repr(e))

	try:
		persona.edad = -5
	except ValueError as e:
		print("Validación de edad negativa ->", repr(e))


def demo_cuenta():
	mostrar_encabezado("Demostración: CuentaBancaria (público, protegido, privado)")
	cuenta = CuentaBancaria(numero_cuenta="ES001", pin_inicial="1234", saldo_inicial=100.0)

	print("Número de cuenta (público):", cuenta.numero_cuenta)
	print("Saldo (property de solo lectura):", cuenta.saldo)

	cuenta.depositar(50)
	print("Saldo tras depósito:", cuenta.consultar_saldo())

	cuenta.retirar(30, pin="1234")
	print("Saldo tras retiro con PIN correcto:", cuenta.consultar_saldo())

	try:
		cuenta.retirar(10, pin="0000")
	except PermissionError as e:
		print("Retiro con PIN incorrecto (esperado) ->", repr(e))

	print("Acceso a _saldo (protegido, no recomendado):", cuenta._saldo)

	try:
		print(cuenta.__pin)
	except AttributeError as e:
		print("Acceso directo a __pin (privado) -> ERROR ESPERADO:", repr(e))


def demo_oficina():
	mostrar_encabezado("Demostración: OficinaBancaria orquestando operaciones")
	oficina = OficinaBancaria(nombre="Oficina Central")
	ana = Persona("Ana", "12345678X", 30)
	bruno = Persona("Bruno", "87654321Y", 28)

	cta_ana = oficina.abrir_cuenta(ana, "ES100", pin_inicial="1111", deposito_inicial=200.0)
	cta_bruno = oficina.abrir_cuenta(bruno, "ES200", pin_inicial="2222", deposito_inicial=75.0)

	print("Total depositado en oficina:", oficina.total_depositado())

	oficina.transferir("ES100", "ES200", 50.0, pin_origen="1111")
	print("Saldo Ana:", cta_ana.consultar_saldo(), "| Saldo Bruno:", cta_bruno.consultar_saldo())

	try:
		oficina.transferir("ES100", "ES200", 10.0, pin_origen="9999")
	except PermissionError as e:
		print("Transferencia con PIN incorrecto ->", repr(e))

	print("Resumen interno (método protegido):", oficina._resumen_interno())
	try:
		print(oficina.__fondos_reserva)
	except AttributeError as e:
		print("Acceso directo a __fondos_reserva (privado) -> ERROR ESPERADO:", repr(e))


def main():
	demo_persona()
	demo_cuenta()
	demo_oficina()


if __name__ == "__main__":
	main()


