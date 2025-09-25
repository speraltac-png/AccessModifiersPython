from presentation.account_vm import CuentaViewModel


class CuentaCLIView:
    """Vista CLI: suscribe a observables y expone un loop simple de demo."""

    def __init__(self, vm: CuentaViewModel):
        self.vm = vm
        self.vm.balance.subscribe(self._render_balance)
        self.vm.error.subscribe(self._render_error)
        self.vm.mensaje.subscribe(self._render_mensaje)

    def _render_balance(self, saldo):
        print(f"Saldo actual: {saldo}")

    def _render_error(self, err):
        if err:
            print(f"[ERROR] {err}")

    def _render_mensaje(self, msg):
        if msg:
            print(f"[INFO] {msg}")

    def demo(self):
        print("=== Demo CLI Cuenta (MVVM) ===")
        print("Comandos: d <monto> | r <monto> <pin> | depositar <monto> | retirar <monto> <pin> | h | q")
        while True:
            try:
                entrada = input("> ").strip()
            except EOFError:
                break
            if not entrada:
                continue
            if entrada.lower() == "q":
                break
            if entrada.lower() in ("h", "help", "ayuda"):
                print("Comandos: d <monto> | r <monto> <pin> | depositar <monto> | retirar <monto> <pin> | q")
                continue
            partes = entrada.split()
            cmd = partes[0].lower()
            if cmd in ("d", "depositar") and len(partes) == 2:
                try:
                    monto = float(partes[1].replace(",", "."))
                    self.vm.depositar(monto)
                except ValueError:
                    print("Uso: d <monto>  |  depositar <monto>")
            elif cmd in ("r", "retirar") and len(partes) == 3:
                try:
                    monto = float(partes[1].replace(",", "."))
                    self.vm.retirar(monto, partes[2])
                except ValueError:
                    print("Uso: r <monto> <pin>  |  retirar <monto> <pin>")
            else:
                print("Comando no reconocido. Escribe 'h' para ayuda.")


