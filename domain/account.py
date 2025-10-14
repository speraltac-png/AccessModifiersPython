class CuentaBancaria:
    """
    Modelo de dominio: Cuenta bancaria con encapsulación por convención
    y name mangling. No depende de UI ni ViewModels.
    """

    def __init__(self, numero_cuenta, titular, pin_inicial):
        self.numero_cuenta = numero_cuenta  # público
        self.titular = titular  # público (por simplicidad)
        self._saldo = 0  # protegido (convención)
        self.__pin = None  # privado (name mangling)
        self.__establecer_pin_inicial(pin_inicial)

    @property
    def saldo(self):
        return self._saldo

    def depositar(self, monto):
        self._validar_monto(monto)
        self._saldo += monto

    def retirar(self, monto, pin):
        self._validar_monto(monto)
        self._requerir_pin(pin)
        if monto > self._saldo:
            raise ValueError("Fondos insuficientes")
        self._saldo -= monto

    def transferir_a(self, otra_cuenta, monto, pin):
        if not isinstance(otra_cuenta, CuentaBancaria):
            raise TypeError("otra_cuenta debe ser CuentaBancaria")
        self.retirar(monto, pin)
        otra_cuenta.depositar(monto)

    def cambiar_pin(self, pin_actual, pin_nuevo):
        self._requerir_pin(pin_actual)
        self._validar_pin_formato(pin_nuevo)
        self.__pin = pin_nuevo

    # --- Protegidos ---
    def _validar_monto(self, monto):
        if not isinstance(monto, (int, float)) or monto <= 0:
            raise ValueError("El monto debe ser un número positivo")

    def _requerir_pin(self, pin):
        if pin != self.__pin:
            raise PermissionError("PIN incorrecto")

    def _validar_pin_formato(self, pin):
        if not isinstance(pin, str) or len(pin) < 4:
            raise ValueError("El PIN debe ser una cadena de 4+ caracteres")

    # --- Privados ---
    def __establecer_pin_inicial(self, pin):
        self._validar_pin_formato(pin)
        self.__pin = pin


    # --- Serialización simple para RTDB ---
    def to_dict(self):
        """
        Serializa el estado público/exportable de la cuenta.
        El PIN no se expone.
        """
        return {
            "numero_cuenta": self.numero_cuenta,
            "titular": self.titular,
            "saldo": self._saldo,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Crea una instancia a partir de un dict. El PIN inicial por defecto es "0000"
        (puedes cambiarlo luego con `cambiar_pin`).
        """
        numero = data.get("numero_cuenta")
        titular = data.get("titular")
        saldo = data.get("saldo", 0)
        inst = cls(numero, titular, "0000")
        # Ajustamos saldo directamente (uso interno controlado)
        inst._saldo = saldo
        return inst

