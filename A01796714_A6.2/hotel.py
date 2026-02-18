import json
import os


class Hotel:

    def __init__(self, hotel_id, name, location, rooms):
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.rooms = rooms

    def create(hotel_id, name, location, rooms):
        data = _load()
        if hotel_id in data["hotels"]:
            print(f"[ERROR] El hotel '{hotel_id}' ya existe.")
            return False
        data["hotels"][hotel_id] = {
            "hotel_id": hotel_id,
            "name": name,
            "location": location,
            "rooms": rooms,
        }
        _save(data)
        return True

    def delete(hotel_id):
        data = _load()
        if hotel_id not in data["hotels"]:
            print(f"[ERROR] Hotel '{hotel_id}' no encontrado.")
            return False
        del data["hotels"][hotel_id]
        _save(data)
        return True

    def get(hotel_id):
        data = _load()
        record = data["hotels"].get(hotel_id)
        if record is None:
            print(f"[ERROR] Hotel '{hotel_id}' no encontrado.")
            return None
        return Hotel(**record)

    def display(hotel_id):
        hotel = Hotel.get(hotel_id)
        if hotel:
            print(f"Hotel        : {hotel.hotel_id}")
            print(f"Nombre       : {hotel.name}")
            print(f"Ubicación    : {hotel.location}")
            print(f"Habitaciones : {hotel.rooms}")

    def modify(hotel_id, **kwargs):
        data = _load()
        if hotel_id not in data["hotels"]:
            print(f"[ERROR] Hotel '{hotel_id}' no encontrado.")
            return False
        allowed = {"name", "location", "rooms"}
        for key, value in kwargs.items():
            if key in allowed:
                data["hotels"][hotel_id][key] = value
            else:
                print(f"[ADVERTENCIA] El campo '{key}' no es modificable.")
        _save(data)
        return True

    def available_rooms(hotel_id):
        data = _load()
        if hotel_id not in data["hotels"]:
            print(f"[ERROR] Hotel '{hotel_id}' no encontrado.")
            return 0
        total = data["hotels"][hotel_id]["rooms"]
        occupied = sum(
            1 for r in data["reservations"].values()
            if r["hotel_id"] == hotel_id and r["status"] == "active"
        )
        return total - occupied
    

DATA_FILE = "tc1.json"

def _load():
    if not os.path.exists(DATA_FILE):
        return {"hotels": {}, "customers": {}, "reservations": {}}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError("El archivo de datos debe ser un JSON.")
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