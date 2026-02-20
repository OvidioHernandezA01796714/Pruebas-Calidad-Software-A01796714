"""Clase Customer (Huésped) con las acciones CRUD para la información del cliente."""

import json
import os


class Customer:
    """Clase que representa un cliente."""
    def __init__(self, customer_id, name, email, phone=""):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone

    def create(customer_id, name, email, phone=""):
        """Acción para registrar un nuevo cliente."""
        data = _load()
        if customer_id in data["customers"]:
            print(f"[ERROR] El cliente '{customer_id}' ya existe.")
            return False
        data["customers"][customer_id] = {
            "customer_id": customer_id,
            "name": name,
            "email": email,
            "phone": phone,
        }
        _save(data)
        return True

    def delete(customer_id):
        """Acción para eliminar un cliente."""
        data = _load()
        if customer_id not in data["customers"]:
            print(f"[ERROR] Cliente '{customer_id}' no encontrado.")
            return False
        del data["customers"][customer_id]
        _save(data)
        return True

    def get(customer_id):
        """Acción para obtener un cliente por su ID."""
        data = _load()
        record = data["customers"].get(customer_id)
        if record is None:
            print(f"[ERROR] Cliente '{customer_id}' no encontrado.")
            return None
        return Customer(**record)

    def display(customer_id):
        """Acción para mostrar la información de un cliente."""
        customer = Customer.get(customer_id)
        if customer:
            print(f"Cliente  : {customer.customer_id}")
            print(f"Nombre   : {customer.name}")
            print(f"Email    : {customer.email}")
            print(f"Teléfono : {customer.phone}")

    def modify(customer_id, **kwargs):
        """Acción para modificar un cliente existente."""
        data = _load()
        if customer_id not in data["customers"]:
            print(f"[ERROR] Cliente '{customer_id}' no encontrado.")
            return False
        allowed = {"name", "email", "phone"}
        for key, value in kwargs.items():
            if key in allowed:
                data["customers"][customer_id][key] = value
            else:
                print(f"[ADVERTENCIA] El campo '{key}' no es modificable.")
        _save(data)
        return True


DATA_FILE = "./test/tc1.json"


def _load():
    """Carga y retorna el diccionario de datos desde un archivo JSON."""
    if not os.path.exists(DATA_FILE):
        return {"hotels": {}, "customers": {}, "reservations": {}}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError("El archivo de datos debe ser un objeto JSON.")
        return data
    except (json.JSONDecodeError, ValueError) as e:
        print(f"[ERROR] No se pudo cargar {DATA_FILE}: {e}")
        return {"hotels": {}, "customers": {}, "reservations": {}}


def _save(data):
    """Guarda el diccionario de datos en un archivo JSON."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except OSError as e:
        print(f"[ERROR] No se pudo guardar {DATA_FILE}: {e}")
