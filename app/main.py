import os
import sys

# Permite ejecutar tanto con `python -m app.main` (recomendado)
# como directamente `python app/main.py` agregando la carpeta raíz al path.
if __package__ in (None, ""):
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from domain.account import CuentaBancaria
from presentation.account_vm import CuentaViewModel
from ui.account_cli import CuentaCLIView


def main():
    # Composición (inyección manual): dominio -> VM -> vista
    cuenta = CuentaBancaria(numero_cuenta="001", titular="Alice", pin_inicial="1234")
    vm = CuentaViewModel(cuenta)
    view = CuentaCLIView(vm)
    view.demo()


if __name__ == "__main__":
    main()


