from .observable import Observable
from domain.account import CuentaBancaria


class CuentaViewModel:
    """ViewModel: expone estado y comandos para la vista."""

    def __init__(self, cuenta: CuentaBancaria):
        self._cuenta = cuenta

        # Estado observable que la UI puede mostrar
        self.balance = Observable(self._cuenta.saldo)
        self.error = Observable(None)
        self.mensaje = Observable(None)

    # --- Comandos ---
    def depositar(self, monto):
        try:
            self.error.value = None
            self._cuenta.depositar(monto)
            self.balance.value = self._cuenta.saldo
            self.mensaje.value = f"Depósito exitoso: +{monto}"
        except Exception as exc:
            self.error.value = str(exc)

    def retirar(self, monto, pin):
        try:
            self.error.value = None
            self._cuenta.retirar(monto, pin)
            self.balance.value = self._cuenta.saldo
            self.mensaje.value = f"Retiro exitoso: -{monto}"
        except Exception as exc:
            self.error.value = str(exc)

    def transferir_a(self, otra_vm, monto, pin):
        if not isinstance(otra_vm, CuentaViewModel):
            raise TypeError("otra_vm debe ser CuentaViewModel")
        try:
            self.error.value = None
            otra_vm.error.value = None
            self._cuenta.transferir_a(otra_vm._cuenta, monto, pin)
            self.balance.value = self._cuenta.saldo
            otra_vm.balance.value = otra_vm._cuenta.saldo
            self.mensaje.value = f"Transferencia enviada: -{monto}"
            otra_vm.mensaje.value = f"Transferencia recibida: +{monto}"
        except Exception as exc:
            self.error.value = str(exc)


