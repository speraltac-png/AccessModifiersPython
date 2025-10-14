import os
import sys
from dotenv import load_dotenv

# Permite ejecutar tanto con `python -m app.main` (recomendado)
# como directamente `python app/main.py` agregando la carpeta raíz al path.
if __package__ in (None, ""):
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from domain.account import CuentaBancaria
from presentation.account_vm import CuentaViewModel
from ui.account_cli import CuentaCLIView
from data.firebase_service import FirebaseRealtimeService


def main():
    # Carga variables de entorno desde .env si existe
    load_dotenv()
    # Composición (inyección manual): dominio -> VM -> vista
    cuenta = CuentaBancaria(numero_cuenta="001", titular="Alice", pin_inicial="1234")
    # Si las variables de entorno de Firebase están configuradas, el servicio funcionará; si no, puedes comentar esta línea.
    storage = None
    try:
        storage = FirebaseRealtimeService(base_path="accounts")
    except Exception:
        storage = None
    vm = CuentaViewModel(cuenta, storage)
    view = CuentaCLIView(vm)
    view.demo()


if __name__ == "__main__":
    main()


