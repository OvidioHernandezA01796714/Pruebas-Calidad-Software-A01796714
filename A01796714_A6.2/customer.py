import json
import os


class Customer:

    def __init__(self, customer_id, name, email, phone=""):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone

    def create(customer_id, name, email, phone=""):
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
        data = _load()
        if customer_id not in data["customers"]:
            print(f"[ERROR] Cliente '{customer_id}' no encontrado.")
            return False
        del data["customers"][customer_id]
        _save(data)
        return True

    @staticmethod
    def get(customer_id):
        data = _load()
        record = data["customers"].get(customer_id)
        if record is None:
            print(f"[ERROR] Cliente '{customer_id}' no encontrado.")
            return None
        return Customer(**record)

    @staticmethod
    def display(customer_id):
        customer = Customer.get(customer_id)
        if customer:
            print(f"Cliente  : {customer.customer_id}")
            print(f"Nombre   : {customer.name}")
            print(f"Email    : {customer.email}")
            print(f"Teléfono : {customer.phone}")

    @staticmethod
    def modify(customer_id, **kwargs):
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


DATA_FILE = "tc.json"


def _load():
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
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except OSError as e:
        print(f"[ERROR] No se pudo guardar {DATA_FILE}: {e}")