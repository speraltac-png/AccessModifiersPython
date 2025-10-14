import json
import os
from typing import Any, Dict, Optional

try:
    import firebase_admin
    from firebase_admin import credentials, db
except Exception:
    firebase_admin = None  # type: ignore
    credentials = None  # type: ignore
    db = None  # type: ignore


class FirebaseRealtimeService:
    """
    Servicio de acceso a Firebase Realtime Database.

    Inicializa con variables de entorno:
    - FIREBASE_CREDENTIALS_JSON: ruta a credenciales JSON o JSON embebido
    - FIREBASE_DB_URL: URL de RTDB (https://<project-id>-default-rtdb.firebaseio.com)
    """

    def __init__(self, base_path: str = "accounts"):
        self._ensure_sdk()
        self.base_path = base_path.strip("/")

    def _ensure_sdk(self):
        if firebase_admin is None:
            raise RuntimeError(
                "firebase-admin no está instalado. Agrega 'firebase-admin' a requirements.txt e instala las dependencias."
            )

        if not firebase_admin._apps:  # type: ignore[attr-defined]
            creds_json = os.environ.get("FIREBASE_CREDENTIALS_JSON")
            db_url = os.environ.get("FIREBASE_DB_URL")
            if not db_url:
                raise RuntimeError("Falta variable de entorno FIREBASE_DB_URL")

            if not creds_json:
                raise RuntimeError("Falta variable de entorno FIREBASE_CREDENTIALS_JSON")

            if os.path.isfile(creds_json):
                cred = credentials.Certificate(creds_json)
            else:
                # Permite pasar el contenido JSON directamente en la variable
                try:
                    parsed = json.loads(creds_json)
                except Exception as exc:  # noqa: BLE001
                    raise RuntimeError("FIREBASE_CREDENTIALS_JSON inválido: no es ruta ni JSON válido") from exc
                cred = credentials.Certificate(parsed)

            firebase_admin.initialize_app(cred, {"databaseURL": db_url})

    # --- CRUD básico ---
    def _ref(self, key: Optional[str] = None):
        path = self.base_path if key is None else f"{self.base_path}/{key}"
        return db.reference(path)

    def create(self, key: str, data: Dict[str, Any]) -> None:
        if not key:
            raise ValueError("key requerida")
        self._ref(key).set(data)

    def read(self, key: str) -> Optional[Dict[str, Any]]:
        if not key:
            raise ValueError("key requerida")
        val = self._ref(key).get()
        if val is None:
            return None
        if not isinstance(val, dict):
            raise ValueError("Formato inesperado en RTDB: se esperaba dict")
        return val

    def update(self, key: str, partial: Dict[str, Any]) -> None:
        if not key:
            raise ValueError("key requerida")
        self._ref(key).update(partial)

    def delete(self, key: str) -> None:
        if not key:
            raise ValueError("key requerida")
        self._ref(key).delete()

    def list_all(self) -> Dict[str, Dict[str, Any]]:
        val = self._ref().get()
        if val is None:
            return {}
        if not isinstance(val, dict):
            raise ValueError("Formato inesperado en RTDB: se esperaba dict de items")
        # Normalizamos solo dicts
        out = {}
        for k, v in val.items():
            if isinstance(v, dict):
                out[k] = v
        return out


