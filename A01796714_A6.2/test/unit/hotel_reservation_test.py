import json
import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import hotel as hotel_mod
import customer as customer_mod
import reservation as reservation_mod


BASE_DIR = os.path.join(os.path.dirname(__file__), '..')    
TEST_FILE = os.path.join(BASE_DIR, "tc1.json")


def use_test_file():
    hotel_mod.DATA_FILE = TEST_FILE
    customer_mod.DATA_FILE = TEST_FILE
    reservation_mod.DATA_FILE = TEST_FILE


def clean():
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


class TestHotel(unittest.TestCase):

    def setUp(self):
        use_test_file()
        clean()

    def tearDown(self):
        clean()

    def test_crear_hotel(self):
        from hotel import Hotel
        self.assertTrue(Hotel.create("H1", "Te big apple", "NYC", 10))

    def test_obtener_hotel(self):
        from hotel import Hotel
        Hotel.create("H1", "Te big apple", "NYC", 10)
        hotel = Hotel.get("H1")
        self.assertEqual(hotel.name, "Te big apple")

    def test_eliminar_hotel(self):
        from hotel import Hotel
        Hotel.create("H1", "Te big apple", "NYC", 10)
        self.assertTrue(Hotel.delete("H1"))
        self.assertIsNone(Hotel.get("H1"))

    def test_modificar_hotel(self):
        from hotel import Hotel
        Hotel.create("H1", "Te big apple", "NYC", 10)
        Hotel.modify("H1", name="Holliday", rooms=20)
        hotel = Hotel.get("H1")
        self.assertEqual(hotel.name, "Holliday")
        self.assertEqual(hotel.rooms, 20)

    def test_mostrar_hotel(self):
        from hotel import Hotel
        Hotel.create("H1", "Te big apple", "NYC", 10)
        Hotel.display("H1")

    def test_habitaciones_disponibles(self):
        from hotel import Hotel
        Hotel.create("H1", "Te big apple", "NYC", 5)
        self.assertEqual(Hotel.available_rooms("H1"), 5)


    def test_crear_hotel_duplicado(self):
        from hotel import Hotel
        Hotel.create("H1", "Te big apple", "NYC", 10)
        self.assertFalse(Hotel.create("H1", "Hilton", "LON", 5))

    def test_eliminar_hotel_inexistente(self):
        from hotel import Hotel
        self.assertFalse(Hotel.delete("hotel1"))

    def test_obtener_hotel_inexistente(self):
        from hotel import Hotel
        self.assertIsNone(Hotel.get("hotel1"))

    def test_modificar_hotel_inexistente(self):
        from hotel import Hotel
        self.assertFalse(Hotel.modify("hotel1", name="X"))

    def test_modificar_campo_no_permitido_hotel(self):
        from hotel import Hotel
        Hotel.create("H1", "Te big apple", "NYC", 10)
        self.assertTrue(Hotel.modify("H1", campo_invalido="x"))

    def test_mostrar_hotel_inexistente(self):
        from hotel import Hotel
        Hotel.display("hotel1")

    def test_habitaciones_disponibles_hotel_inexistente(self):
        from hotel import Hotel
        self.assertEqual(Hotel.available_rooms("hotel1"), 0)


class TestCustomer(unittest.TestCase):

    def setUp(self):
        use_test_file()
        clean()

    def tearDown(self):
        clean()

    def test_crear_cliente(self):
        from customer import Customer
        self.assertTrue(Customer.create("C1", "Mario Jimenez", "mjim@gmail.com", "2352-8685"))

    def test_obtener_cliente(self):
        from customer import Customer
        Customer.create("C1", "Mario Jimenez", "mjim@gmail.com")
        self.assertEqual(Customer.get("C1").name, "Mario Jimenez")

    def test_eliminar_cliente(self):
        from customer import Customer
        Customer.create("C1", "Mario Jimenez", "mjim@gmail.com")
        self.assertTrue(Customer.delete("C1"))
        self.assertIsNone(Customer.get("C1"))

    def test_modificar_cliente(self):
        from customer import Customer
        Customer.create("C1", "Mario Jimenez", "mjim@gmail.com")
        Customer.modify("C1", name="Mario Alberto Jimenez", phone="9636-5547")
        c = Customer.get("C1")
        self.assertEqual(c.name, "Mario Alberto Jimenez")
        self.assertEqual(c.phone, "9636-5547")

    def test_mostrar_cliente(self):
        from customer import Customer
        Customer.create("C1", "Mario Jimenez", "mjim@gmail.com")
        Customer.display("C1")

    def test_crear_cliente_duplicado(self):
        from customer import Customer
        Customer.create("C1", "Mario Jimenez", "mjim@gmail.com")
        self.assertFalse(Customer.create("C1", "Jorge Diaz", "georgeD@gmail.com"))

    def test_eliminar_cliente_inexistente(self):
        from customer import Customer
        self.assertFalse(Customer.delete("customer1"))

    def test_obtener_cliente_inexistente(self):
        from customer import Customer
        self.assertIsNone(Customer.get("customer1"))

    def test_modificar_cliente_inexistente(self):
        from customer import Customer
        self.assertFalse(Customer.modify("customer1", name="X"))

    def test_modificar_campo_no_permitido_cliente(self):
        from customer import Customer
        Customer.create("C1", "Mario Jimenez", "mjim@gmail.com")
        self.assertTrue(Customer.modify("C1", campo_invalido="x"))

    def test_mostrar_cliente_inexistente(self):
        from customer import Customer
        Customer.display("customer1")


class TestReservation(unittest.TestCase):

    def setUp(self):
        use_test_file()
        clean()
        from hotel import Hotel
        from customer import Customer
        Hotel.create("H1", "Te big apple", "NYC", 3)
        Customer.create("C1", "Mario Jimenez", "mjim@gmail.com")

    def tearDown(self):
        clean()

    def test_crear_reservacion(self):
        from reservation import Reservation
        self.assertTrue(
            Reservation.create("R1", "C1", "H1", "10/04/2026", "25/04/2026")
        )

    def test_obtener_reservacion(self):
        from reservation import Reservation
        Reservation.create("R1", "C1", "H1", "10/04/2026", "25/04/2026")
        res = Reservation.get("R1")
        self.assertEqual(res.hotel_id, "H1")
        self.assertEqual(res.status, "activo")

    def test_cancelar_reservacion(self):
        from reservation import Reservation
        Reservation.create("R1", "C1", "H1", "10/04/2026", "25/04/2026")
        self.assertTrue(Reservation.cancel("R1"))
        self.assertEqual(Reservation.get("R1").status, "cancelado")

    def test_mostrar_reservacion(self):
        from reservation import Reservation
        Reservation.create("R1", "C1", "H1", "10/04/2026", "25/04/2026")
        Reservation.display("R1")

    def test_habitaciones_disminuyen_al_reservar(self):
        from reservation import Reservation
        from hotel import Hotel
        Reservation.create("R1", "C1", "H1", "10/04/2026", "25/04/2026")
        self.assertEqual(Hotel.available_rooms("H1"), 2)

    def test_habitaciones_se_restauran_al_cancelar(self):
        from reservation import Reservation
        from hotel import Hotel
        Reservation.create("R1", "C1", "H1", "10/04/2026", "25/04/2026")
        Reservation.cancel("R1")
        self.assertEqual(Hotel.available_rooms("H1"), 3)

    def test_crear_reservacion_duplicada(self):
        from reservation import Reservation
        Reservation.create("R1", "C1", "H1", "10/04/2026", "25/04/2026")
        self.assertFalse(
            Reservation.create("R1", "C1", "H1", "10/04/2026", "25/04/2026")
        )

    def test_crear_reservacion_cliente_inexistente(self):
        from reservation import Reservation
        self.assertFalse(
            Reservation.create("R1", "customer1", "H1", "10/04/2026", "25/04/2026")
        )

    def test_crear_reservacion_hotel_inexistente(self):
        from reservation import Reservation
        self.assertFalse(
            Reservation.create("R1", "C1", "hotel1", "10/04/2026", "25/04/2026")
        )

    def test_crear_reservacion_sin_habitaciones(self):
        from hotel import Hotel
        from customer import Customer
        from reservation import Reservation
        Hotel.create("HHTTLL", "Boutique Hotel", "BCN", 1)
        Customer.create("C2", "Jorge Diaz", "jdiaz@gmail.com")
        Reservation.create("R1", "C1", "HHTTLL", "10/04/2026", "25/04/2026")
        self.assertFalse(
            Reservation.create("R2", "C2", "HHTTLL", "10/04/2026", "25/04/2026")
        )

    def test_cancelar_reservacion_inexistente(self):
        from reservation import Reservation
        self.assertFalse(Reservation.cancel("RV1"))

    def test_cancelar_reservacion_ya_cancelada(self):
        from reservation import Reservation
        Reservation.create("R1", "C1", "H1", "10/04/2026", "25/04/2026")
        Reservation.cancel("R1")
        self.assertFalse(Reservation.cancel("R1"))

    def test_obtener_reservacion_inexistente(self):
        from reservation import Reservation
        self.assertIsNone(Reservation.get("RV1"))

    def test_mostrar_reservacion_inexistente(self):
        from reservation import Reservation
        Reservation.display("RV1")

    def test_json_corrupto_retorna_estructura_vacia(self):
        from reservation import Reservation
        with open(TEST_FILE, "w") as f:
            f.write("{json no valido}")
        self.assertFalse(
            Reservation.create("R1", "C1", "H1", "10/04/2026", "25/04/2026")
        )

    def test_tipo_incorrecto_en_archivo(self):
        from hotel import Hotel
        with open(TEST_FILE, "w") as f:
            json.dump([1, 2, 3], f)
        self.assertIsNone(Hotel.get("H1"))


if __name__ == "__main__":
    unittest.main()
