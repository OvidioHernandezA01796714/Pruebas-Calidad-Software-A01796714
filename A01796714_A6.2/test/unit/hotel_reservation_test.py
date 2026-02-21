"""Tests unitarios para las clases Hotel, Customer y Reservation."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import unittest
import hotel as hotel_mod
import customer as customer_mod
import reservation as reservation_mod

from hotel import Hotel
from customer import Customer
from reservation import Reservation


BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
TEST_FILE = os.path.join(BASE_DIR, "tc1.json")


def use_test_file():
    """Redirige el archivo de datos a uno exclusivo para pruebas."""
    hotel_mod.DATA_FILE = TEST_FILE
    customer_mod.DATA_FILE = TEST_FILE
    reservation_mod.DATA_FILE = TEST_FILE


def clean():
    """Elimina el archivo de prueba entre tests."""
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


class TestHotel(unittest.TestCase):
    """Pruebas unitarias para la clase Hotel."""

    def setUp(self):
        """Configura el entorno antes de cada prueba."""
        use_test_file()
        clean()

    def tearDown(self):
        """Limpia el entorno después de cada prueba."""
        clean()

    def test_crear_hotel(self):
        """Verifica que se puede crear un hotel correctamente."""
        self.assertTrue(Hotel.create("H1", "Te big apple", "NYC", 10))

    def test_obtener_hotel(self):
        """Verifica que se puede obtener un hotel por ID."""
        Hotel.create("H1", "Te big apple", "NYC", 10)
        hotel = Hotel.get("H1")
        self.assertEqual(hotel.name, "Te big apple")

    def test_eliminar_hotel(self):
        """Verifica que se puede eliminar un hotel existente."""
        Hotel.create("H1", "Te big apple", "NYC", 10)
        self.assertTrue(Hotel.delete("H1"))
        self.assertIsNone(Hotel.get("H1"))

    def test_modificar_hotel(self):
        """Verifica que se pueden modificar campos del hotel."""
        Hotel.create("H1", "Te big apple", "NYC", 10)
        Hotel.modify("H1", name="Holliday", rooms=20)
        hotel = Hotel.get("H1")
        self.assertEqual(hotel.name, "Holliday")
        self.assertEqual(hotel.rooms, 20)

    def test_mostrar_hotel(self):
        """Verifica que display no lanza excepción."""
        Hotel.create("H1", "Te big apple", "NYC", 10)
        Hotel.display("H1")

    def test_habitaciones_disponibles(self):
        """Verifica el conteo de habitaciones disponibles."""
        Hotel.create("H1", "Te big apple", "NYC", 5)
        self.assertEqual(Hotel.available_rooms("H1"), 5)

    def test_crear_hotel_duplicado(self):
        """Verifica que no se puede crear un hotel con ID duplicado."""
        Hotel.create("H1", "Te big apple", "NYC", 10)
        self.assertFalse(Hotel.create("H1", "Hilton", "LON", 5))

    def test_eliminar_hotel_inexistente(self):
        """Verifica que eliminar un hotel inexistente retorna False."""
        self.assertFalse(Hotel.delete("hotel1"))

    def test_obtener_hotel_inexistente(self):
        """Verifica que obtener un hotel inexistente retorna None."""
        self.assertIsNone(Hotel.get("hotel1"))

    def test_modificar_hotel_inexistente(self):
        """Verifica que modificar un hotel inexistente retorna False."""
        self.assertFalse(Hotel.modify("hotel1", name="X"))

    def test_modificar_campo_no_permitido_hotel(self):
        """Verifica que modificar un campo no permitido no falla."""
        Hotel.create("H1", "Te big apple", "NYC", 10)
        self.assertTrue(Hotel.modify("H1", campo_invalido="x"))

    def test_mostrar_hotel_inexistente(self):
        """Verifica que display con ID inexistente no lanza excepción."""
        Hotel.display("hotel1")

    def test_habitaciones_disponibles_hotel_inexistente(self):
        """Verifica que available_rooms retorna 0 para hotel inexistente."""
        self.assertEqual(Hotel.available_rooms("hotel1"), 0)


class TestCustomer(unittest.TestCase):
    """Pruebas unitarias para la clase Customer."""

    def setUp(self):
        """Configura el entorno antes de cada prueba."""
        use_test_file()
        clean()

    def tearDown(self):
        """Limpia el entorno después de cada prueba."""
        clean()

    def test_crear_cliente(self):
        """Verifica que se puede crear un cliente correctamente."""
        self.assertTrue(
            Customer.create(
                "C1", "Mario Jimenez", "mjim@gmail.com", "2352-8685")
        )

    def test_obtener_cliente(self):
        """Verifica que se puede obtener un cliente por ID."""
        Customer.create("C1", "Mario Jimenez", "mjim@gmail.com")
        self.assertEqual(Customer.get("C1").name, "Mario Jimenez")

    def test_eliminar_cliente(self):
        """Verifica que se puede eliminar un cliente existente."""
        Customer.create("C1", "Mario Jimenez", "mjim@gmail.com")
        self.assertTrue(Customer.delete("C1"))
        self.assertIsNone(Customer.get("C1"))

    def test_modificar_cliente(self):
        """Verifica que se pueden modificar campos del cliente."""
        Customer.create("C1", "Mario Jimenez", "mjim@gmail.com")
        Customer.modify("C1", name="Mario Alberto Jimenez", phone="9636-5547")
        cliente = Customer.get("C1")
        self.assertEqual(cliente.name, "Mario Alberto Jimenez")
        self.assertEqual(cliente.phone, "9636-5547")

    def test_mostrar_cliente(self):
        """Verifica que display no lanza excepción."""
        Customer.create("C1", "Mario Jimenez", "mjim@gmail.com")
        Customer.display("C1")

    def test_crear_cliente_duplicado(self):
        """Verifica que no se puede crear un cliente con ID duplicado."""
        Customer.create("C1", "Mario Jimenez", "mjim@gmail.com")
        self.assertFalse(
            Customer.create("C1", "Jorge Diaz", "georgeD@gmail.com")
        )

    def test_eliminar_cliente_inexistente(self):
        """Verifica que eliminar un cliente inexistente retorna False."""
        self.assertFalse(Customer.delete("customer1"))

    def test_obtener_cliente_inexistente(self):
        """Verifica que obtener un cliente inexistente retorna None."""
        self.assertIsNone(Customer.get("customer1"))

    def test_modificar_cliente_inexistente(self):
        """Verifica que modificar un cliente inexistente retorna False."""
        self.assertFalse(Customer.modify("customer1", name="X"))

    def test_modificar_campo_no_permitido_cliente(self):
        """Verifica que modificar un campo no permitido no falla."""
        Customer.create("C1", "Mario Jimenez", "mjim@gmail.com")
        self.assertTrue(Customer.modify("C1", campo_invalido="x"))

    def test_mostrar_cliente_inexistente(self):
        """Verifica que display con ID inexistente no lanza excepción."""
        Customer.display("customer1")


class TestReservation(unittest.TestCase):
    """Pruebas unitarias para la clase Reservation."""

    def setUp(self):
        """Configura el entorno y crea hotel y cliente base."""
        use_test_file()
        clean()
        Hotel.create("H1", "Te big apple", "NYC", 3)
        Customer.create("C1", "Mario Jimenez", "mjim@gmail.com")

    def tearDown(self):
        """Limpia el entorno después de cada prueba."""
        clean()

    def test_crear_reservacion(self):
        """Verifica que se puede crear una reservación correctamente."""
        self.assertTrue(
            Reservation.create("R1", "C1", "H1", "10/04/2026", "25/04/2026")
        )

    def test_obtener_reservacion(self):
        """Verifica que se puede obtener una reservación por ID."""
        Reservation.create("R1", "C1", "H1", "10/04/2026", "25/04/2026")
        res = Reservation.get("R1")
        self.assertEqual(res.hotel_id, "H1")
        self.assertEqual(res.status, "activa")

    def test_cancelar_reservacion(self):
        """Verifica que se puede cancelar una reservación activa."""
        Reservation.create("R1", "C1", "H1", "10/04/2026", "25/04/2026")
        self.assertTrue(Reservation.cancel("R1"))
        self.assertEqual(Reservation.get("R1").status, "cancelada")

    def test_mostrar_reservacion(self):
        """Verifica que display no lanza excepción."""
        Reservation.create("R1", "C1", "H1", "10/04/2026", "25/04/2026")
        Reservation.display("R1")

    def test_habitaciones_disminuyen_al_reservar(self):
        """Verifica que las habitaciones disponibles disminuyen al reservar."""
        Reservation.create("R1", "C1", "H1", "10/04/2026", "25/04/2026")
        self.assertEqual(Hotel.available_rooms("H1"), 2)

    def test_habitaciones_se_restauran_al_cancelar(self):
        """Verifica que las habitaciones se restauran al cancelar."""
        Reservation.create("R1", "C1", "H1", "10/04/2026", "25/04/2026")
        Reservation.cancel("R1")
        self.assertEqual(Hotel.available_rooms("H1"), 3)

    def test_crear_reservacion_duplicada(self):
        """Verifica que no se puede crear una reservación con ID duplicado."""
        Reservation.create("R1", "C1", "H1", "10/04/2026", "25/04/2026")
        self.assertFalse(
            Reservation.create("R1", "C1", "H1", "10/04/2026", "25/04/2026")
        )

    def test_crear_reservacion_cliente_inexistente(self):
        """Verifica que no se puede reservar con un cliente inexistente."""
        self.assertFalse(
            Reservation.create(
                "R1", "customer1", "H1", "10/04/2026", "25/04/2026")
        )

    def test_crear_reservacion_hotel_inexistente(self):
        """Verifica que no se puede reservar en un hotel inexistente."""
        self.assertFalse(
            Reservation.create(
                "R1", "C1", "hotel1", "10/04/2026", "25/04/2026")
        )

    def test_crear_reservacion_sin_habitaciones(self):
        """Verifica que no se puede reservar si no hay habitaciones."""
        Hotel.create("HHTTLL", "Boutique Hotel", "BCN", 1)
        Customer.create("C2", "Jorge Diaz", "jdiaz@gmail.com")
        Reservation.create("R1", "C1", "HHTTLL", "10/04/2026", "25/04/2026")
        self.assertFalse(
            Reservation.create(
                "R2", "C2", "HHTTLL", "10/04/2026", "25/04/2026")
        )

    def test_cancelar_reservacion_inexistente(self):
        """Verifica que cancelar una reservación inexistente retorna False."""
        self.assertFalse(Reservation.cancel("RV1"))

    def test_cancelar_reservacion_ya_cancelada(self):
        """Verifica que no se puede cancelar una reservación ya cancelada."""
        Reservation.create("R1", "C1", "H1", "10/04/2026", "25/04/2026")
        Reservation.cancel("R1")
        self.assertFalse(Reservation.cancel("R1"))

    def test_obtener_reservacion_inexistente(self):
        """Verifica que obtener una reservación inexistente retorna None."""
        self.assertIsNone(Reservation.get("RV1"))

    def test_mostrar_reservacion_inexistente(self):
        """Verifica que display con ID inexistente no lanza excepción."""
        Reservation.display("RV1")

    def test_json_corrupto_retorna_estructura_vacia(self):
        """Verifica que un JSON corrupto es manejado sin lanzar excepción."""
        with open(TEST_FILE, "w", encoding="utf-8") as f:
            f.write("{json no valido}")
        self.assertFalse(
            Reservation.create("R1", "C1", "H1", "10/04/2026", "25/04/2026")
        )

    def test_tipo_incorrecto_en_archivo(self):
        """
        Verifica que un JSON con tipo incorrecto es manejado correctamente.
        """
        with open(TEST_FILE, "w", encoding="utf-8") as f:
            json.dump([1, 2, 3], f)
        self.assertIsNone(Hotel.get("H1"))


if __name__ == "__main__":
    unittest.main()
