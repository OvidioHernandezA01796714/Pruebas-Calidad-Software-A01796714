import json
import os

from hotel import Hotel


class Reservation:
    def __init__(self, reservation_id, customer_id, hotel_id,
                 check_in, check_out, status="active"):
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id
        self.check_in = check_in
        self.check_out = check_out
        self.status = status

    def create(reservation_id, customer_id, hotel_id, check_in, check_out):
        data = _load()

        if reservation_id in data["reservations"]:
            print(f"[ERROR] La reservación '{reservation_id}' ya existe.")
            return False

        if customer_id not in data["customers"]:
            print(f"[ERROR] Cliente '{customer_id}' no encontrado.")
            return False

        if hotel_id not in data["hotels"]:
            print(f"[ERROR] Hotel '{hotel_id}' no encontrado.")
            return False

        if Hotel.available_rooms(hotel_id) <= 0:
            print(
                f"[ERROR] No hay habitaciones disponibles "
                f"en el hotel '{hotel_id}'."
            )
            return False

        data["reservations"][reservation_id] = {
            "reservation_id": reservation_id,
            "customer_id": customer_id,
            "hotel_id": hotel_id,
            "check_in": check_in,
            "check_out": check_out,
            "status": "active",
        }
        _save(data)
        return True

    def cancel(reservation_id):
        data = _load()
        if reservation_id not in data["reservations"]:
            print(f"[ERROR] Reservación '{reservation_id}' no encontrada.")
            return False
        if data["reservations"][reservation_id]["status"] == "cancelled":
            print(
                f"[ERROR] La reservación '{reservation_id}' "
                f"ya está cancelada."
            )
            return False
        data["reservations"][reservation_id]["status"] = "cancelled"
        _save(data)
        return True

    def get(reservation_id):
        data = _load()
        record = data["reservations"].get(reservation_id)
        if record is None:
            print(f"[ERROR] Reservación '{reservation_id}' no encontrada.")
            return None
        return Reservation(**record)

    def display(reservation_id):
        res = Reservation.get(reservation_id)
        if res:
            print(f"Reservación  : {res.reservation_id}")
            print(f"Cliente      : {res.customer_id}")
            print(f"Hotel        : {res.hotel_id}")
            print(f"Check-in     : {res.check_in}")
            print(f"Check-out    : {res.check_out}")
            print(f"Estado       : {res.status}")


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