from .observable import Observable
from domain.account import CuentaBancaria
from data.firebase_service import FirebaseRealtimeService


class CuentaViewModel:
    """ViewModel: expone estado y comandos para la vista."""

    def __init__(self, cuenta: CuentaBancaria, storage: FirebaseRealtimeService | None = None):
        self._cuenta = cuenta
        self._storage = storage

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

    # --- CRUD en Firebase ---
    def guardar(self):
        """Crea/actualiza en RTDB por `numero_cuenta`."""
        if not self._storage:
            self.error.value = "Storage no configurado"
            return
        try:
            key = self._cuenta.numero_cuenta
            self._storage.create(key, self._cuenta.to_dict())
            self.mensaje.value = f"Cuenta {key} guardada"
        except Exception as exc:
            self.error.value = str(exc)

    def cargar(self, numero_cuenta):
        if not self._storage:
            self.error.value = "Storage no configurado"
            return
        try:
            data = self._storage.read(numero_cuenta)
            if not data:
                self.error.value = "No encontrada"
                return
            self._cuenta = CuentaBancaria.from_dict(data)
            self.balance.value = self._cuenta.saldo
            self.mensaje.value = f"Cuenta {numero_cuenta} cargada"
        except Exception as exc:
            self.error.value = str(exc)

    def eliminar(self, numero_cuenta):
        if not self._storage:
            self.error.value = "Storage no configurado"
            return
        try:
            self._storage.delete(numero_cuenta)
            self.mensaje.value = f"Cuenta {numero_cuenta} eliminada"
        except Exception as exc:
            self.error.value = str(exc)

    def listar(self):
        if not self._storage:
            self.error.value = "Storage no configurado"
            return {}
        try:
            return self._storage.list_all()
        except Exception as exc:
            self.error.value = str(exc)
            return {}


